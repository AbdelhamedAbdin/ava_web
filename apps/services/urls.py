from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet
from django.urls import path

app_name = 'apps.services'


urlpatterns = [
    path('', ServiceViewSet.as_view({'get': 'list','post': 'create'}), name='businessview'),
    path('<int:pk>', ServiceViewSet.as_view({'get': 'retrieve','put': 'update',
            'patch': 'update','delete': 'destroy'}), name='businessdetailview')
]