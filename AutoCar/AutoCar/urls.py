from django.contrib import admin
from django.urls import path, include
from .views import landing_page, about_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landingpage'),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    path('cars/', include('cars.urls')),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Change 'login' to '/'
    path('about/', about_view, name='about'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)