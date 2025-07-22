from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class SharedAccount(models.Model):
    """
    Model for shared saving accounts.
    Multiple users can contribute to and borrow from this account.
    """
    
    ACCOUNT_TYPES = [
        ('family', 'Family Account'),
        ('friends', 'Friends Account'),
        ('business', 'Business Account'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    # Basic information
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='family')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Financial information
    balance = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    target_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Members and permissions
    members = models.ManyToManyField(User, through='AccountMembership')
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_accounts'
    )
    
    # Settings
    allow_loans = models.BooleanField(default=True)
    max_loan_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    min_contribution = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('10.00'),
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shared_accounts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.account_type})"
    
    def get_total_contributions(self):
        """Get total contributions to this account."""
        return self.transactions.filter(
            transaction_type='contribution'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    def get_total_loans(self):
        """Get total outstanding loans from this account."""
        from loans.models import Loan
        return Loan.objects.filter(
            account=self, 
            status='active'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    def get_available_balance(self):
        """Get available balance for loans (balance - outstanding loans)."""
        return self.balance - self.get_total_loans()
    
    def can_borrow(self, amount):
        """Check if the account can provide a loan of the specified amount."""
        if not self.allow_loans:
            return False
        
        available_balance = self.get_available_balance()
        if available_balance < amount:
            return False
        
        if self.max_loan_amount and amount > self.max_loan_amount:
            return False
        
        return True
    
    def add_member(self, user, role='member'):
        """Add a member to the account."""
        membership, created = AccountMembership.objects.get_or_create(
            account=self,
            user=user,
            defaults={'role': role}
        )
        return membership
    
    def remove_member(self, user):
        """Remove a member from the account."""
        try:
            membership = AccountMembership.objects.get(account=self, user=user)
            membership.delete()
            return True
        except AccountMembership.DoesNotExist:
            return False


class AccountMembership(models.Model):
    """
    Through model for User-SharedAccount relationship.
    Defines roles and permissions for account members.
    """
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    account = models.ForeignKey(SharedAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    # Permissions
    can_contribute = models.BooleanField(default=True)
    can_borrow = models.BooleanField(default=True)
    can_invite = models.BooleanField(default=False)
    can_manage = models.BooleanField(default=False)
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'account_memberships'
        unique_together = ['account', 'user']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.account.name} ({self.role})"
    
    def save(self, *args, **kwargs):
        """Set permissions based on role."""
        if self.role == 'owner':
            self.can_contribute = True
            self.can_borrow = True
            self.can_invite = True
            self.can_manage = True
        elif self.role == 'admin':
            self.can_contribute = True
            self.can_borrow = True
            self.can_invite = True
            self.can_manage = True
        elif self.role == 'member':
            self.can_contribute = True
            self.can_borrow = True
            self.can_invite = False
            self.can_manage = False
        elif self.role == 'viewer':
            self.can_contribute = False
            self.can_borrow = False
            self.can_invite = False
            self.can_manage = False
        
        super().save(*args, **kwargs)
