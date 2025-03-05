   # AutoCar/recommendations/admin.py
from django.contrib import admin
from .models import SurveyResponse

admin.site.register(SurveyResponse)  # Register the SurveyResponse model