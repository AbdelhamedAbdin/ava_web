from decimal import Decimal
from django.db.models import Sum
from django.db import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
    
# App Imports
from .choices import StateChoices, StateCollectionChoices
# External Apps Imports
from apps.clients.models import Client
from apps.services.models import Service


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client", null=True)
    project_name = models.CharField(max_length=200)
    total_value = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Total Value", blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=4, decimal_places=2 , verbose_name="Tax Percentage", blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Tax Amount", blank=True, null=True)
    total_after_tax = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Total After Tax", blank=True, null=True)
    total_collections = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Total Collections", blank=True, null=True)
    total_collected = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Total Collections", blank=True, null=True)
    total_collectable = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Total Collectable", blank=True, null=True)
    state = models.CharField(max_length=11, choices=StateChoices.choices)
    
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Remaining Balance", blank=True, null=True)
    
    start_date = models.DateField(verbose_name="Project Start Date", blank=True, null=True)
    end_date = models.DateField(verbose_name="Project End Date", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)
    
    def __str__(self):
        return str(self.project_name)
    
    def save(self, *args, **kwargs):
        if self.projectservices.exists():
            self.total_value = self.projectservices.filter(total_service_price__isnull = False).aggregate(Sum('total_service_price'))['total_service_price__sum']
            # This Condition Is For Preventing the Cration Of Project Services Without Inputting Tax-Percentage
            if self.tax_percentage is None:
                raise serializers.ValidationError({'tax_percentage': ['Tax Can\'t Be Empty']},code='invalid')
            
            if self.tax_percentage > 0 and self.total_value is not None:
                if self.total_value > 0:
                    self.tax_amount = (self.total_value * self.tax_percentage) / 100
                    self.total_after_tax = self.total_value - self.tax_amount
                    if self.projectcollections_set.all().exists():
                        self.total_collections = self.projectcollections_set.filter(amount__isnull = False).aggregate(Sum('amount'))['amount__sum']
                        self.total_collectable = self.total_after_tax - self.total_collections
                        self.total_collected =  self.projectcollections_set.filter(state=StateCollectionChoices.COLLECTED).aggregate(Sum('amount'))['amount__sum']
                        if self.total_collected is not None:
                            self.remaining_balance = self.total_after_tax - self.total_collected
                        else:
                            self.remaining_balance = self.total_after_tax
                    else:
                        self.remaining_balance = self.total_after_tax
                    
            elif self.tax_percentage == 0 and self.total_value is not None:
                self.tax_amount = 0
                if self.total_value > 0:
                    self.total_after_tax = self.total_value
                    if self.projectcollections_set.all().exists():
                        self.total_collections = self.projectcollections_set.filter(amount__isnull = False).aggregate(Sum('amount'))['amount__sum']
                        self.total_collectable = self.total_after_tax - self.total_collections
                        collected = self.projectcollections_set.filter(state=StateCollectionChoices.COLLECTED).aggregate(Sum('amount'))['amount__sum']
                        if collected is not None:
                            self.remaining_balance = self.total_after_tax - collected
                        else:
                            self.remaining_balance = self.total_after_tax
                    else:
                        self.remaining_balance = self.total_after_tax
        super().save(*args, **kwargs)


class ProjectService(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="projectservices")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="project_service")
    count = models.PositiveIntegerField(default=1)
    total_service_price = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="Total Service Price", blank=True, null=True)
    
    class Meta:
        unique_together = [
            ("project", "service"),
        ]
    
    def __str__(self):
        return f'{self.project} | {self.service}'
        
    def save(self, *args, **kwargs):
        if self.count > 0:
            self.total_service_price = Decimal(self.count)*Decimal(self.service.price)
            #For DashBoard
            # self.service.servicedash.update_or_create(service=self.service, user=self.service.user)
        elif self.count <= 0:
            raise serializers.ValidationError({'count': ['Count Must Be Postive Int Value']},code='invalid')
        super().save(*args, **kwargs)
    
    
class ProjectCollections(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="Amount")
    collection_date = models.DateField(verbose_name="Collection Date",)
    state = models.CharField(max_length=10, choices=StateCollectionChoices.choices)
    
    def __str__(self):
        return f'{self.project} | {self.amount} | {self.collection_date}'
    
    def save(self, *args, **kwargs):
        if self.amount > 0:
            if self.project.total_value is None:
                raise serializers.ValidationError({'You Can\'t add a Collection Without Adding Service To The Project'},code='invalid')
            if self.project.total_collections is not None:
                if not self.amount <= self.project.total_collectable:
                    raise serializers.ValidationError({'amount': [f'Your Remaining Collectable Project Balance is {self.project.total_collectable} you cann\'t overlimit it']},code='invalid')
            else:
                if not self.amount <= self.project.total_after_tax:
                    raise serializers.ValidationError({'amount': [f'Your Available Collectable Project Balance is {self.project.total_after_tax} you cann\'t overlimit it']},code='invalid')
        elif self.amount <= 0:
            raise serializers.ValidationError({'amount': ['Amount Must Be A Postive Int']},code='invalid')
        super().save(*args, **kwargs)