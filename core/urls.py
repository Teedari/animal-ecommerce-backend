from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path

from core.settings import DEBUG

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

if DEBUG:
    from django.conf.urls import handler403
    handler403 = 'account.views.view.error403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('account.urls', namespace='account')),
    path('api/v1/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('api.urls', namespace='api')),
    path('', include('dashboard.urls', namespace='dashboard')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


