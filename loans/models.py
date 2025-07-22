from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Loan(models.Model):
    """
    Model for interest-free loans from shared accounts.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('repaid', 'Repaid'),
        ('overdue', 'Overdue'),
        ('defaulted', 'Defaulted'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Loan details
    account = models.ForeignKey(
        'accounts.SharedAccount',
        on_delete=models.CASCADE,
        related_name='loans'
    )
    borrower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Terms
    term_months = models.PositiveIntegerField(default=12)
    monthly_payment = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Dates
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    repaid_at = models.DateTimeField(null=True, blank=True)
    
    # Financial tracking
    amount_paid = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    remaining_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Approval information
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_loans'
    )
    approval_notes = models.TextField(blank=True)
    
    # Metadata
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['borrower', 'status']),
            models.Index(fields=['account', 'status']),
            models.Index(fields=['due_date', 'status']),
        ]
    
    def __str__(self):
        return f"Loan {self.reference_number} - {self.borrower.username} - {self.amount}"
    
    def save(self, *args, **kwargs):
        """Generate reference number and calculate monthly payment."""
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        
        if self.amount and self.term_months and not self.monthly_payment:
            self.monthly_payment = self.amount / self.term_months
        
        if not self.remaining_balance:
            self.remaining_balance = self.amount
        
        super().save(*args, **kwargs)
    
    def generate_reference_number(self):
        """Generate a unique reference number for the loan."""
        import uuid
        return f"LOAN-{uuid.uuid4().hex[:8].upper()}"
    
    def approve(self, approved_by, notes=""):
        """Approve the loan."""
        from django.utils import timezone
        self.status = 'approved'
        self.approved_by = approved_by
        self.approval_notes = notes
        self.approved_at = timezone.now()
        self.save()
    
    def disburse(self):
        """Disburse the loan amount."""
        from django.utils import timezone
        from datetime import date, timedelta
        
        if self.status != 'approved':
            raise ValueError("Loan must be approved before disbursement")
        
        # Check if account has sufficient balance
        if not self.account.can_borrow(self.amount):
            raise ValueError("Insufficient account balance for loan disbursement")
        
        self.status = 'active'
        self.disbursed_at = timezone.now()
        self.due_date = date.today() + timedelta(days=30 * self.term_months)
        self.save()
        
        # Create disbursement transaction
        from transactions.models import Transaction
        Transaction.objects.create(
            account=self.account,
            transaction_type='loan_disbursement',
            amount=self.amount,
            description=f"Loan disbursement for {self.purpose}",
            status='completed',
            initiated_by=self.borrower,
            recipient=self.borrower,
            related_loan=self,
            balance_before=self.account.balance,
            balance_after=self.account.balance - self.amount
        )
    
    def make_payment(self, amount, payment_date=None):
        """Make a payment towards the loan."""
        from django.utils import timezone
        from transactions.models import Transaction
        
        if self.status not in ['active', 'overdue']:
            raise ValueError("Can only make payments on active or overdue loans")
        
        if amount > self.remaining_balance:
            raise ValueError("Payment amount exceeds remaining balance")
        
        self.amount_paid += amount
        self.remaining_balance -= amount
        
        if self.remaining_balance <= 0:
            self.status = 'repaid'
            self.repaid_at = timezone.now()
        
        self.save()
        
        # Create repayment transaction
        Transaction.objects.create(
            account=self.account,
            transaction_type='loan_repayment',
            amount=amount,
            description=f"Loan repayment for {self.reference_number}",
            status='completed',
            initiated_by=self.borrower,
            recipient=None,
            related_loan=self,
            balance_before=self.account.balance,
            balance_after=self.account.balance + amount
        )
    
    def get_loan_summary(self):
        """Get a summary of the loan for display."""
        return {
            'id': self.id,
            'reference_number': self.reference_number,
            'amount': self.amount,
            'purpose': self.purpose,
            'status': self.status,
            'borrower': self.borrower.full_name,
            'term_months': self.term_months,
            'monthly_payment': self.monthly_payment,
            'amount_paid': self.amount_paid,
            'remaining_balance': self.remaining_balance,
            'due_date': self.due_date,
            'created_at': self.created_at,
        }
