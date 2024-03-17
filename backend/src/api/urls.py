from django.urls import include, path
from dotenv import load_dotenv
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
import os

# swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

load_dotenv()

API_SWAGGER_ON = os.getenv('API_SWAGGER_ON', 'False').lower() == 'true'

schema_view = get_schema_view(
    openapi.Info(
        title="OVO Hunters API",
        default_version="",
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=API_SWAGGER_ON,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [    
    path("", include("django_prometheus.urls")),
    
    path("backend/api/ovo-hunters_auth/", include("apps.ovohunters_auth.urls")),
    path("backend/api/ovo-hunters_starthack/", include("apps.ovohunters_starthack.urls")),
    
    path('backend/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('backend/api/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('backend/api/api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)