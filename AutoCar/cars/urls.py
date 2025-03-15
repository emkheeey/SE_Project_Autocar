from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('compare/', views.compare_cars, name='compare_cars'),
]