from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Transaction(models.Model):
    """
    Model for tracking all financial transactions in shared accounts.
    """
    
    TRANSACTION_TYPES = [
        ('contribution', 'Contribution'),
        ('withdrawal', 'Withdrawal'),
        ('loan_disbursement', 'Loan Disbursement'),
        ('loan_repayment', 'Loan Repayment'),
        ('transfer', 'Transfer'),
        ('fee', 'Fee'),
        ('refund', 'Refund'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Transaction details
    account = models.ForeignKey(
        'accounts.SharedAccount', 
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # User information
    initiated_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='initiated_transactions'
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='received_transactions',
        null=True, 
        blank=True
    )
    
    # Related loan (if applicable)
    related_loan = models.ForeignKey(
        'loans.Loan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    # Balance tracking
    balance_before = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Metadata
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['account', 'transaction_type']),
            models.Index(fields=['initiated_by', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.name}"
    
    def save(self, *args, **kwargs):
        """Generate reference number and update account balance."""
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        
        # Update account balance based on transaction type
        if self.status == 'completed':
            self.update_account_balance()
        
        super().save(*args, **kwargs)
    
    def generate_reference_number(self):
        """Generate a unique reference number for the transaction."""
        import uuid
        return f"TXN-{uuid.uuid4().hex[:8].upper()}"
    
    def update_account_balance(self):
        """Update the account balance based on transaction type."""
        account = self.account
        
        if self.transaction_type in ['contribution', 'loan_repayment', 'refund']:
            account.balance += self.amount
        elif self.transaction_type in ['withdrawal', 'loan_disbursement', 'fee']:
            account.balance -= self.amount
        
        account.save()
    
    def get_transaction_summary(self):
        """Get a summary of the transaction for display."""
        return {
            'id': self.id,
            'type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'status': self.status,
            'initiated_by': self.initiated_by.full_name,
            'created_at': self.created_at,
            'reference_number': self.reference_number,
        }
