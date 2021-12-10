from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from apps.dashboards.models import ExpenseDash

# App Imports
from .models import ExpenseCategory, Payment, PaymentSummary
from .serializers import ExpenseCategorySerializer, PaymentSerializer, PaymentSummarySerializer


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExpenseCategorySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        category = get_object_or_404(ExpenseCategory.objects.filter(id=self.kwargs["pk"]))
        if category is not None and self.request.user == category.user:
            return category
        elif category is not None and self.request.user != category.user:
            raise PermissionDenied('You Have No Permission To Access this Expenses Category')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(ExpenseCategory.objects.filter(user=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # ExpenseDash.objects.get(user=self.request.user).save()
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


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        payment = get_object_or_404(Payment.objects.filter(id=self.kwargs["pk"]))
        if payment is not None and self.request.user == payment.user:
            return payment
        elif payment is not None and self.request.user != payment.user:
            raise PermissionDenied('You Have No Permission To Access this Client')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(Payment.objects.filter(state=self.kwargs["state"], user=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class PaymentSummaryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentSummarySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options',]
    
    def get_object(self, queryset=None, **kwargs):
        summary = get_object_or_404(PaymentSummary.objects.filter(payment__pk=self.kwargs["pk"], id=self.kwargs["num"]))
        if summary is not None and self.request.user == summary.user:
            return summary
        elif summary is not None and self.request.user != summary.user:
            raise PermissionDenied('You Have No Permission To Access this Payment')
        else:
            raise PermissionDenied('Bad Request')

    def get_queryset(self):
        return get_list_or_404(PaymentSummary.objects.filter(payment__pk=self.kwargs["pk"], user=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        try:
            ExpenseDash.objects.get(user=self.request.user).save()
        except:
            ExpenseDash.objects.create(user=self.request.user)
            ExpenseDash.objects.get(user=self.request.user).save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        payment = get_object_or_404(Payment.objects.filter(id=self.kwargs["pk"], user=self.request.user))
        serializer.save(payment=payment, user=self.request.user)
        payment.save()

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, instance)
        ExpenseDash.objects.get(user=self.request.user).save()
        return Response(serializer.data)
    
    def perform_update(self, serializer, instance):
        serializer.save()
        instance.payment.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        payment = instance.payment
        self.perform_destroy(instance)
        payment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)