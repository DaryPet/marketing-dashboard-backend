
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from backend.users.views import RegisterView


# Configuration for the Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Marketing Dashboard API",  # Title of the API
        default_version='v1',  # API version
        description="API for managing marketing campaigns and channels",  # Brief description of the API
    ),
    public=True,  # Makes the documentation publicly accessible
    permission_classes=(permissions.AllowAny,),  # No restrictions on accessing the documentation
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', RegisterView.as_view(), name='register'), 
    path('', include('backend.campaigns.urls')),
    # path('', include('backend.users.urls')),
    path('api/users/', include('backend.users.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
]
