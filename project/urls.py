from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hotel.views import components

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('hotel.urls')),
    path('', include('clients.urls')),
    path('', include('analytics.urls')),
    path('components/', components, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
