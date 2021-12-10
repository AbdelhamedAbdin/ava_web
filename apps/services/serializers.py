from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.income.models import ProjectService
from .models import Service
from .choices import ServiceTypeChoices

   
class ServiceSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Service
        fields = ['id', 'business', 'service_name', 'service_description', 'service_type', 'unit_name', 'price']
        read_only_fields = ('id', 'business',)
        depth = 0

        extra_kwargs = {
            'service_name':        {'allow_null': False, 'allow_blank': False, 'required': True},
            'service_description': {'allow_null': True, 'allow_blank': True, 'required': False},
            'service_type':        {'allow_null': False, 'allow_blank': False, 'required': True},
            'unit_name':           {'allow_null': True, 'allow_blank': True, 'required': False},
            'price':               {'required': True}
            }

    