from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('hotel.urls')),
    path('', include('clients.urls')),
    path('', include('analytics.urls')),
    path(
        'error/',
        TemplateView.as_view(template_name="general/error.html"),
        name='error'
    ),
    path(
        'contacts/',
        TemplateView.as_view(template_name="general/contacts.html"),
        name='contacts'
    ),
    path(
        'about/',
        TemplateView.as_view(template_name="general/about.html"),
        name='about'
    ),
    path(
        'success/',
        TemplateView.as_view(template_name="general/booking_success.html"),
        name='success'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)