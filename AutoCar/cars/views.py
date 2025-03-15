from django.shortcuts import render
from .models import Car
from django.views.generic import ListView

class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

def compare_cars(request):
    car_ids = request.GET.getlist('car_id')
    cars = Car.objects.filter(id__in=car_ids)
    
    # Get all unique feature categories across selected cars
    all_features = set()
    for car in cars:
        # Add any feature categories you want to compare
        if car.safety_features:
            all_features.update(car.safety_features.split(','))
    
    context = {
        'cars': cars,
        'all_features': sorted(all_features)
    }
    return render(request, 'cars/compare.html', context)