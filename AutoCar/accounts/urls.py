from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from accounts.views import about_view

urlpatterns = [
    path('home/', views.home, name='accounts_home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/variants-json/<int:car_id>/', views.car_variants_json, name='car_variants_json'),
    path('cars/debug/<int:car_id>/', views.debug_car_detail, name='debug_car_detail'),
    path('cars/fix-variants/', views.fix_variant_relationships, name='fix_variants'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('diagnostics/', views.error_handler, name='diagnostics'),
    path('minimal/', views.minimal_view, name='minimal'),
    path('about/', views.about_view, name='about'),
    path('update_car_image/', views.update_car_image, name='update_car_image'),
    path('debug/', views.debug_info, name='debug_info'),
    path('static-test/', views.debug_static, name='debug_static'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('compare/', views.compare_cars, name='compare'),
]