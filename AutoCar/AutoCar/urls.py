from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
import os
import sys
import traceback
import logging
from django.conf import settings
from django.contrib.auth.views import LogoutView
from accounts import views  # Add this import
from AutoCar.utils.supabase_utils import get_supabase_client

# Configure logging
logger = logging.getLogger(__name__)

def health_check(request):
    """
    Extremely simple health check endpoint
    """
    return HttpResponse("OK", content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('cars/', views.cars, name='cars'),
    path('cars/debug-info/', views.debug_car_info, name='debug_car_info'),
    path('logout/', views.logout_view, name='logout'),
    path('base/', views.base_view, name='base'),
    path('minimal/', views.minimal_view, name='minimal'),
    path('error/', views.error_handler, name='error_handler'),
    path('debug-static/', views.debug_static, name='debug_static'),
    path('debug-info/', views.debug_info, name='debug_info'),
    path('accounts/cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('accounts/cars/debug/<int:car_id>/', views.debug_car_detail, name='debug_car_detail'),
    path('accounts/cars/variants-json/<int:car_id>/', views.car_variants_json, name='car_variants_json'),
    path('accounts/fix-variants/', views.fix_variant_relationships, name='fix_variants'),
    path('health/', health_check, name='health_check'),  # Simple health check
]