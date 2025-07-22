from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model for SharedSaver application.
    Extends Django's AbstractUser with additional fields for fintech functionality.
    """
    
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Additional fields
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Financial information
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('employed', 'Employed'),
            ('self_employed', 'Self Employed'),
            ('unemployed', 'Unemployed'),
            ('student', 'Student'),
            ('retired', 'Retired'),
        ],
        default='employed'
    )
    
    # Account status
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_total_savings(self):
        """Get total savings across all shared accounts."""
        from accounts.models import SharedAccount
        return SharedAccount.objects.filter(members=self).aggregate(
            total=models.Sum('balance')
        )['total'] or 0
    
    def get_total_loans(self):
        """Get total outstanding loans."""
        from loans.models import Loan
        return Loan.objects.filter(borrower=self, status='active').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
