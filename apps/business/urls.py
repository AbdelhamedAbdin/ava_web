from .views import BusinessViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'apps.business'


urlpatterns = [
    path('', BusinessViewSet.as_view(), name='businessview')
]
