from django.db import models

# Create your models here.
class StateChoices(models.TextChoices):
        REMAINING = 'remaining', 'Remaining'
        PAID = 'paid', 'Paid'
        
        
class StateSummaryChoices(models.TextChoices):
        PAID = 'paid', 'Paid'
        PENDING = 'pending', 'Pending'
