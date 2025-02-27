from django.urls import path
from .views import register, profile, user_login
from django.contrib.auth.views import LogoutView

urlpatterns = [
       path('register/', register, name='register'),
       path('profile/', profile, name='profile'),
       path('login/', user_login, name='login'),  # Add this line
       path('logout/', LogoutView.as_view(), name='logout'),
   ]