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
    path('', views.base_view, name='base'),  # Add the base view at root URL
    path('accounts/', include('accounts.urls')),  # Include accounts URLs with prefix
    path('health/', health_check, name='health_check'),  # Simple health check
]