from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('compare/', views.compare_cars, name='compare_cars'),
    path('load-data/', views.load_cars_from_json_view, name='load_cars'),
    path('clear/', views.clear_cars, name='clear_cars'),  # Add this line
    path('search/', views.search_cars, name='search_cars'),
]