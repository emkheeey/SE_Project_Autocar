from django.shortcuts import render
from django.views.generic import ListView
from .models import Car
import json
import os

# Import the utility function - place this at the top
from .load_data import load_cars_from_json as load_cars_data

class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We'll let the user explicitly load data using the button
        return context

def compare_cars(request):
    car_ids = request.GET.getlist('car_id')
    cars = Car.objects.filter(id__in=car_ids)
    
    # Define all the spec categories and their importance (weight for scoring)
    spec_categories = [
        # Price & Value (lower is better)
        {'name': 'Price (PHP)', 'key': 'price', 'format': 'currency', 'weight': 10, 'lower_better': True},
        
        # Performance metrics (higher is usually better)
        {'name': 'Horsepower', 'key': 'horsepower', 'format': 'number', 'weight': 8, 'lower_better': False},
        {'name': 'Engine', 'key': 'engine', 'format': 'text', 'weight': 7, 'comparable': False},
        {'name': 'Transmission', 'key': 'transmission', 'format': 'text', 'weight': 6, 'comparable': False},
        {'name': 'Drivetrain', 'key': 'drivetrain', 'format': 'text', 'weight': 5, 'comparable': False},
        
        # Practicality & Comfort
        {'name': 'Body Type', 'key': 'body_type', 'format': 'text', 'weight': 4, 'comparable': False},
        {'name': 'Number of Seats', 'key': 'seats', 'format': 'text', 'weight': 7, 'comparable': False},
        {'name': 'Fuel Type', 'key': 'fuel_type', 'format': 'text', 'weight': 6, 'comparable': False},
        {'name': 'Wheel Size', 'key': 'wheel_size', 'format': 'text', 'weight': 3, 'comparable': False},
        
        # Features
        {'name': 'Safety Features', 'key': 'safety_features', 'format': 'text', 'weight': 9, 'comparable': False},
        {'name': 'Technology Features', 'key': 'technology_features', 'format': 'text', 'weight': 8, 'comparable': False},
        {'name': 'Warranty', 'key': 'warranty', 'format': 'text', 'weight': 7, 'comparable': False},
    ]
    
    # Calculate scores for each car
    car_scores = []
    for car in cars:
        score = {
            'car': car,
            'total_score': 0,
            'performance_score': 0,
            'value_score': 0,
            'comfort_score': 0,
            'feature_score': 0,
            'winning_categories': [],
        }
        car_scores.append(score)
    
    # Calculate scores for each comparable specification
    for category in spec_categories:
        if category.get('comparable', True):
            values = [getattr(car, category['key'], None) for car in cars]
            valid_values = [v for v in values if v is not None]
            
            if valid_values:
                # For numeric values, score based on where in the range they fall
                try:
                    numeric_values = [float(v) for v in valid_values]
                    min_val = min(numeric_values)
                    max_val = max(numeric_values)
                    range_val = max_val - min_val if max_val > min_val else 1
                    
                    for i, car in enumerate(cars):
                        value = getattr(car, category['key'], None)
                        if value is not None:
                            try:
                                value = float(value)
                                # Calculate score 0-10 where 10 is best
                                if category.get('lower_better', False):
                                    # Lower is better (like price)
                                    normalized_score = (max_val - value) / range_val * 10
                                else:
                                    # Higher is better (like horsepower)
                                    normalized_score = (value - min_val) / range_val * 10
                                
                                # Add weighted score to total
                                weighted_score = normalized_score * (category.get('weight', 5) / 10)
                                car_scores[i]['total_score'] += weighted_score
                                
                                # Categorize the score
                                if category['key'] in ['price']:
                                    car_scores[i]['value_score'] += weighted_score
                                elif category['key'] in ['horsepower', 'engine']:
                                    car_scores[i]['performance_score'] += weighted_score
                                elif category['key'] in ['seats', 'body_type']:
                                    car_scores[i]['comfort_score'] += weighted_score
                                else:
                                    car_scores[i]['feature_score'] += weighted_score
                                    
                                # Track if this is the best car in this category
                                is_best = (category.get('lower_better', False) and value == min_val) or \
                                         (not category.get('lower_better', False) and value == max_val)
                                if is_best:
                                    car_scores[i]['winning_categories'].append(category['name'])
                            except (ValueError, TypeError):
                                pass
                except (ValueError, TypeError):
                    pass
    
    # Normalize and round scores for display
    max_score = max([score['total_score'] for score in car_scores]) if car_scores else 1
    for score in car_scores:
        score['total_score'] = round((score['total_score'] / max_score) * 100)
        score['performance_score'] = round(score['performance_score'] * 10)
        score['value_score'] = round(score['value_score'] * 10)
        score['comfort_score'] = round(score['comfort_score'] * 10)
        score['feature_score'] = round(score['feature_score'] * 10)
    
    # Sort car scores by total score (highest first)
    car_scores.sort(key=lambda x: x['total_score'], reverse=True)
    
    context = {
        'cars': cars,
        'spec_categories': spec_categories,
        'car_scores': car_scores,
        'car_count': len(cars),
        'best_car': car_scores[0]['car'] if car_scores else None,
    }
    return render(request, 'cars/compare.html', context)

# HTTP request handler for loading JSON data
def load_cars_from_json_view(request):
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        'toyota_cars_data.json'
    )
    
    if not os.path.exists(json_path):
        return render(request, 'cars/message.html', {
            'message': 'JSON file not found. Please run the scraper first.'
        })
    
    # Call the utility function from load_data.py
    count = load_cars_data(json_path)
    
    return render(request, 'cars/message.html', {
        'message': f'Successfully loaded {count} cars from JSON file.'
    })
    
# Add this to your existing views.py file
def clear_cars(request):
    """Delete all cars from the database"""
    if request.method == 'POST':
        # Delete all cars
        deleted_count = Car.objects.all().delete()[0]
        return render(request, 'cars/message.html', {
            'message': f'Successfully deleted {deleted_count} cars from the database.'
        })
    else:
        # Show confirmation page
        car_count = Car.objects.count()
        return render(request, 'cars/confirm_delete.html', {
            'car_count': car_count
        })