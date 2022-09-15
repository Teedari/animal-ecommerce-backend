from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path

from core.settings import DEBUG

if DEBUG:
    from django.conf.urls import handler403
    handler403 = 'account.views.view.error403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('account.urls', namespace='account')),
    path('api/v1/', include('api.urls', namespace='api')),
    path('', include('dashboard.urls', namespace='dashboard')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


