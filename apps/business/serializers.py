from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['business_title', 'country', 'currency']
        depth = 1
        
        extra_kwargs = {
            'business_title': {'allow_null': False, 'allow_blank': False, 'required': True},
            'country':        {'required': True},
            'currency':       {'required': True}
            }
