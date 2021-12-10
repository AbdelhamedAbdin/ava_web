from django.urls.conf import path
from .views import ClientViewSet, ClientFilterView
# from django.urls import path
from .models import Client

app_name = 'apps.clients'


urlpatterns = [
    path('', ClientViewSet.as_view({'get': 'list','post': 'create'}), name='businessview'),
    path('<int:pk>', ClientViewSet.as_view({'get': 'retrieve','put': 'update',
            'patch': 'update', 'delete': 'destroy'}), name='businessdetailview'),
    path('search/', ClientFilterView.as_view(), name='clientfilterview'),
]