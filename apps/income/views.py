from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError

#App Imports
from .models import Project, ProjectCollections, ProjectService
from .serializers import ProjectSerializer, ProjectCollectionsSerializer, ProjectServiceSerializer
from apps.dashboards.models import ProjectsIncomeDash
#Extrnal App Imports
from apps.dashboards.models import ServiceIncomeDash
from apps.dashboards.serializers import ServiceIncomeDashSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        client = get_object_or_404(Project.objects.filter(id=self.kwargs["pk"]))
        if client is not None and self.request.user == client.user:
            return client
        elif client is not None and self.request.user != client.user:
            raise PermissionDenied('You Have No Permission To Access this Client')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        print(Project.objects.filter(user=self.request.user))
        return get_list_or_404(Project.objects.filter(user=self.request.user))

    def create(self, request, *args, **kwargs):
        # print(request.data["projectservice"])
        # append to first key in list 
        # crete dictionary and .update to add the old dict to it 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, pk=None):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer, pk=None):
        serializer.save(user=self.request.user)


class ProjectServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectServiceSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        projectsrv = get_object_or_404(ProjectService.objects.filter(project__pk=self.kwargs["pk"], id=self.kwargs["num"]))
        if projectsrv is not None and self.request.user == projectsrv.project.user:
            return projectsrv
        elif projectsrv is not None and self.request.user != projectsrv.user:
            raise PermissionDenied('You Have No Permission To Access this Project Service')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(ProjectService.objects.filter(project__pk=self.kwargs["pk"], project__user=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        try:
            project = get_object_or_404(Project.objects.filter(id=self.kwargs["pk"]))
            serializer.save(project=project)
            project.save()
            
        except IntegrityError:
            raise ValidationError({'service': ['This Service already exists In the Project']}, code='invalid')

            
    def update(self, request, *args, **kwargs):
        if "service" in request.data:
            raise ValidationError({'service': ["Service Already Sent In Url 'Not Allowed' "]}, code='invalid')
        else:
            partial = True
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer, instance)
            return Response(serializer.data)
    
    def perform_update(self, serializer, instance):
        # Not Needed Any More Was Just For Catching Unique Integrity only
        try:
            serializer.save()
            instance.project.save()
        except IntegrityError:
            raise ValidationError({'service': ['Project with this Service already exists.']}, code='invalid')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project = instance.project
        self.perform_destroy(instance)
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProjectCollectionsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectCollectionsSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        project = get_object_or_404(ProjectCollections.objects.filter(project__pk=self.kwargs["pk"], id=self.kwargs["num"]))
        if project is not None and self.request.user == project.project.user:
            return project
        elif project is not None and self.request.user != project.user:
            raise PermissionDenied('You Have No Permission To Access this Client')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(ProjectCollections.objects.filter(project__pk=self.kwargs["pk"], project__user=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        try:
            ProjectsIncomeDash.objects.get(user=self.request.user).save()
        except:
            ProjectsIncomeDash.objects.create(user=self.request.user)
            ProjectsIncomeDash.objects.get(user=self.request.user).save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        project = get_object_or_404(Project.objects.filter(id=self.kwargs["pk"], user=self.request.user))
        serializer.save(project=project)
        project.save()

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, instance)
        ProjectsIncomeDash.objects.get(user=self.request.user).save()
        return Response(serializer.data)
    
    def perform_update(self, serializer, instance):
        serializer.save()
        instance.project.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project = instance.project
        self.perform_destroy(instance)
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)