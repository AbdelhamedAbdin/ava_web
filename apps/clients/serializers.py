from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'company_name', 'email', 'phone']
        read_only_fields = ('id',)
        depth = 1
        
        extra_kwargs = {
            'client_name':  {'allow_null': False, 'allow_blank': False, 'required': True},
            'company_name': {'allow_null': False, 'allow_blank': False, 'required': True},
            'email':        {'allow_null': False, 'allow_blank': False, 'required': True},
            'phone':        {'allow_null': False, 'allow_blank': False, 'required': True}
            }
