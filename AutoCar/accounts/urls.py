from django.urls import path
from .views import register, profile, user_login
from django.contrib.auth.views import LogoutView
from .views import browse_view, home_view 
from django.contrib.auth import views as auth_views


urlpatterns = [
       path('register/', register, name='register'),
       path('profile/', profile, name='profile'),
       path('login/', user_login, name='login'),  # Add this line
       path('logout/', LogoutView.as_view(), name='logout'),
       path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),  # Login URL
       path('', home_view, name='home'),
       path('browse/', browse_view, name='browse'),
   ]