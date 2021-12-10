from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, bad_request

from apps.services.choices import ServiceTypeChoices
## App Imports ##
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ServiceSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]

    def get_object(self, queryset=None, **kwargs):
        service = get_object_or_404(Service.objects.filter(id=self.kwargs["pk"]))
        if service is not None and self.request.user == service.user:
            return service
        elif service is not None and self.request.user != service.user:
            raise PermissionDenied('You Have No Permission To Access this Service')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(Service.objects.filter(user=self.request.user))
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, business=self.request.user.business)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer, instance):
        project = instance.project_service
        project_names = instance.project_service.all().values_list('project__project_name', flat=True)
        project_names_list = list(project_names)
        if project.exists():
            raise PermissionDenied(f'This Service Belong To Projects {project_names_list} Try Deleting Them First')
        else:
            serializer.save(user=self.request.user, business=self.request.user.business)

    def destroy(self, request,  *args, **kwargs):
        instance = self.get_object()
        project = instance.project_service
        project_names = instance.project_service.all().values_list('project__project_name', flat=True)
        project_names_list = list(project_names)
        if project.exists():
            raise PermissionDenied(f'This Service Belong To Projects {project_names_list} Try Deleting Them First')
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    