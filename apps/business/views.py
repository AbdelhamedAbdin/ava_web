from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.exceptions import PermissionDenied
## App Imports ##
from .models import Business
from .serializers import BusinessSerializer


# Create your views here.
class BusinessViewSet(CreateAPIView, RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BusinessSerializer
    http_method_names = ['get', 'post', 'put', 'options',] # 'patch', 'delete', 'head',  'trace'

    def get_object(self, queryset=None, **kwargs):
        business = get_object_or_404(Business.objects.filter(user=self.request.user))
        if business is not None and self.request.user == business.user:
            return business
        else:
            raise PermissionDenied('Bad Request')

    def create(self, request, *args, **kwargs):
        if Business.objects.filter(user=self.request.user).exists():
            raise PermissionDenied('You Already Have a Business')
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    