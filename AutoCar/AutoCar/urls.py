from django.contrib import admin
from django.urls import path, include
from .views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    path('browse/', include('accounts.urls')),
    
]
