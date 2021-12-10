from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProjectsIncomeDash, ServiceIncomeDash, ExpenseDash, ExpenseIncomeDash, CashFlowDash
User = get_user_model()
## App Imports ##


class ProjectsIncomeDashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsIncomeDash
        fields = ['id', 'user', 'total_collecetd_projects', 'total_remaining_projects']
        read_only_fields = ['id', 'user', 'total_collecetd_projects', 'total_remaining_projects']
        depth = 0


class ServiceIncomeDashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceIncomeDash
        fields = ['id', 'user', 'service', 'total_for_service', 'highest_service']
        
        read_only_fields = ['id', 'user', 'service', 'total_for_service', 'highest_service']
        depth = 0
        
        
class ExpenseDashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseDash
        fields = ['id', 'user', 'paid_exp_cat', 'remaining_exp_cat']
        read_only_fields = ['id', 'user', 'paid_exp_cat', 'remaining_exp_cat']
        depth = 0
        
        
class ExpenseIncomeDashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseIncomeDash
        fields = ['id', 'user', 'expense_cat', 'total_for_category']
        read_only_fields = ['id', 'user', 'expense_cat', 'total_for_category']
        depth = 0

        
class CashFlowDashSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowDash
        fields = ['id', 'user']
        read_only_fields = ['id', 'user']
        depth = 0
