from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from rest_framework import serializers
User = get_user_model()

import decimal
## App Imports ##
from .choices import StateChoices, StateSummaryChoices


# Create your models here.
class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(verbose_name="Created At",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At",auto_now=True)
    
    def __str__(self):
        return str(self.name)
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    
    payment_name = models.CharField(max_length=50)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    summaries_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining = models.DecimalField(max_digits=10, decimal_places=2,  blank=True, null=True)
    
    startdate = models.DateField()
    enddate = models.DateField()
    
    state = models.CharField(max_length=10, choices=StateChoices.choices)
    
    created_at = models.DateTimeField(verbose_name="Created At",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At",auto_now=True)

    def __str__(self):
        return str(self.payment_name)
    

    def save(self, *args, **kwargs):
        if self.total_expense_amount > 0:
            self.remaining = self.total_expense_amount
            self.summaries_amount = self.payment_summary.filter(amount__isnull = False).aggregate(Sum('amount'))['amount__sum']
            if self.summaries_amount is not None:
                self.payable_amount = self.total_expense_amount - self.summaries_amount
            self.paid_amount = self.payment_summary.filter(state=StateSummaryChoices.PAID, amount__isnull = False).aggregate(Sum('amount'))['amount__sum']
            
            if self.paid_amount is not None:
                self.remaining = self.total_expense_amount - self.paid_amount
        elif self.total_expense_amount <= 0:
            raise serializers.ValidationError({'total_expense_amount': ['Total Expense Amount Must Be A Postive Int']}, code='invalid')
        super().save(*args, **kwargs)
    
class PaymentSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment_summary')
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=10, choices=StateSummaryChoices.choices)
    
    created_at = models.DateTimeField(verbose_name="Created At",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At",auto_now=True)
    
    def __str__(self):
        return f'{self.payment} | {self.amount}'

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise serializers.ValidationError({'amount': ['Wrong Payment Amount Input']}, code='invalid')
        elif self.amount > 0:
            if self.payment.summaries_amount:
                if not self.amount <= self.payment.payable_amount:
                    raise serializers.ValidationError({'amount': [f'Your Total Remaining Expense Amount is {self.payment.payable_amount} you cann\'t overlimit it']}, code='invalid')     
            else:
                if not self.amount <= self.payment.total_expense_amount:
                    raise serializers.ValidationError({'amount': [f'Your Total Remaining Expense Amount is {self.payment.total_expense_amount} you cann\'t overlimit it']}, code='invalid')
        super().save(*args, **kwargs)
