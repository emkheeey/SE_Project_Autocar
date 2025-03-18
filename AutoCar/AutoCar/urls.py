from django.contrib import admin
from django.urls import path, include
from .views import landing_page, about_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    path('cars/', include('cars.urls')),
    path('about/', about_view, name='about'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)