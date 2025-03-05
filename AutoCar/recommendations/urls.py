   # AutoCar/recommendations/urls.py
from django.urls import path
from .views import survey_view, success_view  # Import the survey view

urlpatterns = [
       path('survey/', survey_view, name='survey_view'),  # Define the survey URL
       path('success/', success_view, name='success'),  # Define the success URL
   ]