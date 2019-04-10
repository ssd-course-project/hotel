from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('hotel.urls')),
    path('', include('clients.urls')),
    path('components/', views.components, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
