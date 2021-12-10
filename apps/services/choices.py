from django.db import models

# Create your models here.
class ServiceTypeChoices(models.TextChoices):
        AMOUNT = 'AM', 'Amount'
        UNITS = 'UN', 'Units'