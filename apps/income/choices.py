from django.db import models

# Create your models here.
class StateChoices(models.TextChoices):
        REMAINING = 'remaining', 'Remaining'
        COLLECTED = 'collected', 'Collected'
        
        
class StateCollectionChoices(models.TextChoices):
        COLLECTED = 'collected', 'Collected'
        PENDING = 'pending', 'Pending'
