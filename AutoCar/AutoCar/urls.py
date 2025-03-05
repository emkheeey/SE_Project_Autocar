from django.contrib import admin
from django.urls import path, include
from .views import landing_page
from recommendations.views import survey_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    path('', include('recommendations.urls')),
    path('recommendations/', include('recommendations.urls')),  
    path('recommendations/survey/', survey_view, name='survey'),  # Correctly reference the survey_view
]
