from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from accounts.views import about_view

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('cars/', views.cars, name='cars'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('diagnostics/', views.error_handler, name='diagnostics'),
    path('minimal/', views.minimal_view, name='minimal'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile, name='profile'),
]