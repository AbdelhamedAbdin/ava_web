from django.urls import path
from .views import ProjectViewSet, ProjectCollectionsViewSet, ProjectServiceViewSet

app_name = 'app.projects'

urlpatterns = [
    path('', ProjectViewSet.as_view({'get': 'list','post': 'create'}), name='projectview'),
    path('<int:pk>', ProjectViewSet.as_view({'get': 'retrieve','put': 'update',
                'patch': 'update','delete': 'destroy'}), name='projectdetailview'),
    
    path('<int:pk>/service/', ProjectServiceViewSet.as_view({'get': 'list','post': 'create'}), name='projectcollectionview'),
    path('<int:pk>/service/<int:num>', ProjectServiceViewSet.as_view({'get': 'retrieve','put': 'update',
                'patch': 'update','delete': 'destroy'}), name='projectservicedetailview'),
    
    path('<int:pk>/summary/', ProjectCollectionsViewSet.as_view({'get': 'list','post': 'create'}), name='projectcollectionview'),
    path('<int:pk>/summary/<int:num>', ProjectCollectionsViewSet.as_view({'get': 'retrieve','put': 'update',
                'patch': 'update','delete': 'destroy'}), name='projectcollectiondetailview')
]
