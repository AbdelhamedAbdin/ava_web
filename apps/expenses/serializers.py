from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
## App Imports ##
from .models import ExpenseCategory, Payment, PaymentSummary


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name',]
        read_only_fields = ['id',]
        depth = 0
        
        extra_kwargs = {
            'name':   {'required': True},
            }


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'startdate', 'expense_category', 'payment_name', 'summaries_amount',
                  'paid_amount','total_expense_amount','remaining', 'enddate', 'state']
        read_only_fields = ['id', 'remaining', 'paid_amount', 'remaining', 'summaries_amount']
        depth = 0
        
        extra_kwargs = {
            'startdate':           {'required': True},
            'expense_category':    {'required': True},
            'payment_name':        {'required': True},
            'total_expense_amount':{'required': True},
            'enddate':             {'required': True},
            'state':               {'required': True},
            }


class PaymentSummarySerializer(serializers.ModelSerializer):
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), required=False)
    class Meta:
        model = PaymentSummary
        fields = ['id', 'payment', 'date', 'amount', 'state',]
        read_only_fields = ['id',]
        depth = 0
        
        extra_kwargs = {
            'payment':{'required': True},
            'date':   {'required': True},
            'amount': {'required': True},
            'state':  {'required': True},
            }
