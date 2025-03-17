from django.contrib import admin
from django.urls import path, include
from .views import landing_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    path('cars/', include('cars.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)