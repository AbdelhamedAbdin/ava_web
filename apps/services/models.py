from django.db import models
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()
# App Imports
from .choices import ServiceTypeChoices
# External Apps Imports
from apps.business.models import Business

# Create your models here.
class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200)
    service_description = models.CharField(max_length=200)
    
    # When Sending Service Type Choices Are: {"AM" - "UN"}
    service_type = models.CharField(max_length=2, choices=ServiceTypeChoices.choices)
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Price")
    
    created_at = models.DateTimeField(verbose_name="Created At",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At",auto_now=True)
    
    def __str__(self):
        return str(self.service_name)

    def save(self, *args, **kwargs):
        if self.price <= 0:
            raise serializers.ValidationError({'price': ['Service Price Must Be Postive Int']},code='invalid')
        elif self.price > 0:
            if self.service_type == ServiceTypeChoices.UNITS:
                if self.unit_name is None:
                    raise serializers.ValidationError({'unit_name': ['Units Must Have A Unit Name']},code='invalid')
            elif self.service_type == ServiceTypeChoices.AMOUNT:
                self.unit_name = None
        super().save(*args, **kwargs)
