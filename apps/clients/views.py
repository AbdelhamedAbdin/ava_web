from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, bad_request
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
## App Imports ##
from .models import Client
from .serializers import ClientSerializer


class ClientFilter(filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'client_name': ['icontains'],
            'company_name': ['icontains'],
            'email': ['icontains'],
            'phone': ['icontains'],
            'created_at': ['iexact', 'lte', 'gte']
        }
    
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        return parent.filter(user=user)

    
class ClientFilterView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_class = ClientFilter


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientSerializer
    # filter_fields = ('client_name', 'company_name', 'email', 'phone')
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        client = get_object_or_404(Client.objects.filter(id=self.kwargs["pk"]))
        if client is not None and self.request.user == client.user:
            return client
        elif client is not None and self.request.user != client.user:
            raise PermissionDenied('You Have No Permission To Access this Client')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(Client.objects.filter(user=self.request.user))

    def create(self, request, *args, **kwargs):
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
