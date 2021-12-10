from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Django API', authentication_classes=[], permission_classes=[])),
    path('api/auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # path('api/auth/', include('rest_framework_social_oauth2.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/authentication/', include('apps.authentication.urls')),
    path('api/business/', include('apps.business.urls')),
    path('api/services/', include('apps.services.urls')),
    path('api/clients/', include('apps.clients.urls')),
    path('api/income/', include('apps.income.urls')),
    path('api/expenses/', include('apps.expenses.urls')),
    path('api/dashboards/', include('apps.dashboards.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
