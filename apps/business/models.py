from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    business_title = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return str(self.business_title)