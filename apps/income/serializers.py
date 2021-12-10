from rest_framework import serializers

## App Imports ##
from .models import Project, ProjectCollections, ProjectService

## External Apps Imports ##
from apps.clients.models import Client


class ProjectServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectService
        fields = ['id', 'service', 'count', 'total_service_price']
        read_only_fields = ['id', 'total_service_price']
        depth = 0
        
        extra_kwargs = {
            'project':  {'required': True},
            'service':  {'required': True},
            'count':    {'required': True}
            }
       

class ProjectCollectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectCollections
        fields = ['id', 'amount', 'collection_date', 'state']
        read_only_fields = ['id',]
        depth = 0
        
        extra_kwargs = {
            'project':         {'required': True},
            'amount':          {'required': True},
            'collection_date': {'required': True},
            'state':           {'required': True},
            }


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=True) 
    projectservice = ProjectServiceSerializer(source="projectservices",
                                                allow_null=False,
                                                read_only=True,
                                                many=True
                                                )
    projectcollections = ProjectCollectionsSerializer(source="projectcollections_set",
                                                allow_null=False,
                                                read_only=True,
                                                many=True
                                                )

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'projectservice' , 'projectcollections' ,'total_value', 'tax_percentage', 'tax_amount', 'remaining_balance', 'total_collectable',
                  'total_after_tax', 'client', 'state', 'start_date', 'end_date']
        read_only_fields = ['id', 'projectservice', 'total_value', 'total_after_tax', 'tax_amount', 'total_collectable', 'remaining_balance']
        depth = 1
        
        extra_kwargs = {
            'project_name':     {'allow_null': False, 'allow_blank': False, 'required': True},
            'tax_percentage':   {'required': False},
            'client':           {'required': True},
            'state':            {'required': True},
            'start_date':       {'required': False},
            'end_date':         {'required': False}
            }
