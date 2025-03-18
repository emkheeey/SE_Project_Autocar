from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('compare/', views.compare_cars, name='compare_cars'),
    path('load-data/', views.load_cars_from_json_view, name='load_cars'),
    path('clear/', views.clear_cars, name='clear_cars'),  # Add this line
    path('search/', views.search_cars, name='search_cars'),
    path('associate-images/', views.associate_car_images, name='associate_car_images'),
    path('<int:car_id>/', views.car_detail, name='car_detail'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)