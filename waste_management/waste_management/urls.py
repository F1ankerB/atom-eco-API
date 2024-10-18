from django.urls import path, re_path
from django.contrib import admin
from core.views import (
    OrganizationListCreateView,
    OrganizationRetrieveUpdateDestroyView,
    StorageListCreateView,
    StorageRetrieveUpdateDestroyView,
    WasteTransferView
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API for managing organizations, storages, waste types, and transfers.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='organization-detail'),
    path('storages/', StorageListCreateView.as_view(), name='storage-list-create'),
    path('storages/<int:pk>/', StorageRetrieveUpdateDestroyView.as_view(), name='storage-detail'),
    path('waste-transfers/', WasteTransferView.as_view(), name='waste-transfer'),
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
