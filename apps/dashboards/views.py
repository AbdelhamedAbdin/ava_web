from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

## App Imports ##
from .models import ProjectsIncomeDash, ExpenseDash, CashFlowDash
from .serializers import ProjectsIncomeDashSerializer, ExpenseDashSerializer, CashFlowDashSerializer


# Create your views here.
class ProjectsIncomeDashView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectsIncomeDashSerializer

    def get_object(self, queryset=None, **kwargs):
        revenue = get_object_or_404(ProjectsIncomeDash.objects.filter(user=self.request.user))
        if revenue is not None and self.request.user == revenue.user:
            return revenue
        else:
            raise PermissionDenied('Bad Request')


# Make the {ServiceIncomeDashView} ListView with any way You Like


class ExpenseDashView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExpenseDashSerializer

    def get_object(self, queryset=None, **kwargs):
        revenue = get_object_or_404(ExpenseDash.objects.filter(user=self.request.user))
        if revenue is not None and self.request.user == revenue.user:
            return revenue
        else:
            raise PermissionDenied('Bad Request')


# Make the {ExpenseIncomeDashView} ListView with any way You Like


class CashFlowDashView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CashFlowDashSerializer

    def get_object(self, queryset=None, **kwargs):
        revenue = get_object_or_404(CashFlowDash.objects.filter(user=self.request.user))
        if revenue is not None and self.request.user == revenue.user:
            return revenue
        else:
            raise PermissionDenied('Bad Request')
