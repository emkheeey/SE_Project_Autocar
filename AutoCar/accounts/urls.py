from django.urls import path
from .views import register, profile, user_login

urlpatterns = [
       path('register/', register, name='register'),
       path('profile/', profile, name='profile'),
       path('login/', user_login, name='login'),  # Add this line
   ]