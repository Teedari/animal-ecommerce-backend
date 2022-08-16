from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='MY API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls', namespace='api')),
    path('', include('dashboard.urls', namespace='dashboard')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


