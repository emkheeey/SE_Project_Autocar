from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Car
from django.db import models
from decimal import Decimal
import json
import os
from .models import Car

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
        
# Add this function to your views.py

def associate_car_images(request):
    """Associate available images with car models in the database"""
    # Get all cars
    cars = Car.objects.all()
    updated_count = 0
    
    # Base path for the static images
    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        'static', 'images', 'cars'
    )
    
    # Get list of available images
    image_files = [f for f in os.listdir(static_dir) if f.endswith('.jpg') or f.endswith('.png')]
    image_names = {os.path.splitext(file)[0].lower(): file for file in image_files}
    
    # Match cars with images
    for car in cars:
        # Try exact match first
        model_key = car.model.lower()
        if model_key in image_names:
            # Found exact match
            car.image_path = f"images/cars/{image_names[model_key]}"
            car.save()
            updated_count += 1
        else:
            # Try partial match
            for img_name in image_names:
                if img_name in model_key or model_key in img_name:
                    car.image_path = f"images/cars/{image_names[img_name]}"
                    car.save()
                    updated_count += 1
                    break
    
    return render(request, 'cars/message.html', {
        'message': f'Successfully associated {updated_count} cars with images.'
    })

def search_cars(request):
    """
    View for searching and filtering cars based on various criteria.
    Handles GET parameters to filter the queryset of Car objects.
    """
    # Start with all cars
    cars = Car.objects.all()
    
    # Track applied filters for the template
    applied_filters = {}
    
    # Text search (model name, description)
    query = request.GET.get('query')
    if query:
        cars = cars.filter(model__icontains=query)
        applied_filters['query'] = query
    
    # Handle price filtering - support both new and old parameter formats
    price_range = request.GET.get('price_range')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # First try the new price_range parameter
    if price_range and price_range != 'all':
        try:
            min_val, max_val = price_range.split('-')
            cars = cars.filter(price__gte=min_val, price__lte=max_val)
            applied_filters['price_range'] = price_range
        except (ValueError, TypeError):
            # If there's an error parsing the range, ignore this filter
            pass
    # Fall back to the old min_price/max_price parameters if price_range is not used
    elif min_price or max_price:
        if min_price:
            try:
                min_price = float(min_price)
                cars = cars.filter(price__gte=min_price)
                applied_filters['min_price'] = min_price
                
                # Create an equivalent price_range for consistency in the UI
                if max_price:
                    max_price = float(max_price)
                    if min_price <= 500000 and max_price >= 500000:
                        applied_filters['price_range'] = '0-500000'
                    elif min_price <= 1000000 and max_price >= 1000000:
                        applied_filters['price_range'] = '500000-1000000'
                    elif min_price <= 1500000 and max_price >= 1500000:
                        applied_filters['price_range'] = '1000000-1500000'
                    elif min_price <= 2000000 and max_price >= 2000000:
                        applied_filters['price_range'] = '1500000-2000000'
                    else:
                        applied_filters['price_range'] = '2000000-999999999'
            except (ValueError, TypeError):
                pass
                
        if max_price:
            try:
                max_price = float(max_price)
                cars = cars.filter(price__lte=max_price)
                applied_filters['max_price'] = max_price
            except (ValueError, TypeError):
                pass
    
    # Body type filter with improved handling for multi-value fields
    body_type = request.GET.get('body_type')
    if body_type and body_type != 'all':
        # Filter for either exact matches or where body_type is part of a multi-value field
        cars = cars.filter(
        models.Q(body_type=body_type) | 
        models.Q(body_type__contains=f"\n{body_type}") | 
        models.Q(body_type__contains=f"{body_type}\n")
    )
    applied_filters['body_type'] = body_type
    
    # Transmission filter - improved handling for multi-value fields
    transmission = request.GET.get('transmission')
    if transmission and transmission != 'all':
        cars = cars.filter(
            models.Q(transmission=transmission) | 
            models.Q(transmission__contains=f"\n{transmission}") | 
            models.Q(transmission__contains=f"{transmission}\n")
        )
        applied_filters['transmission'] = transmission

    # Extract unique transmissions from the database - improved to match JSON format
    raw_transmissions = Car.objects.values_list('transmission', flat=True).distinct()
    transmissions = set()
    for t in raw_transmissions:
        if t and '\n' in t:
            # Split multi-value transmissions and add each one individually
            for tx in t.split('\n'):
                if tx.strip():  # Only add non-empty values
                    transmissions.add(tx.strip())
        elif t:
            transmissions.add(t)

    # Convert to sorted list for the template
    transmissions = sorted(transmissions)
    
    # Sort options
    sort_by = request.GET.get('sort', 'model')  # Default sort by model
    sort_direction = request.GET.get('direction', 'asc')
    
    # Handle sort direction
    if sort_direction == 'desc':
        sort_parameter = f"-{sort_by}"
    else:
        sort_parameter = sort_by
        
    cars = cars.order_by(sort_parameter)
    applied_filters['sort'] = sort_by
    applied_filters['direction'] = sort_direction
    
    # Extract unique body types directly from the database
    # This ensures we only show body types that actually exist
    raw_body_types = Car.objects.values_list('body_type', flat=True).distinct()
    
    # Process the raw body types to handle any with newline characters
    body_types = set()
    for bt in raw_body_types:
        if bt and '\n' in bt:
            # Split multi-value body types and add each one
            body_types.update([b.strip() for b in bt.split('\n')])
        elif bt:
            body_types.add(bt)
    
    # Convert to sorted list for the template
    body_types = sorted(body_types)
    
    # Similar handling for transmissions
    raw_transmissions = Car.objects.values_list('transmission', flat=True).distinct()
    transmissions = set()
    for t in raw_transmissions:
        if t and '\n' in t:
            transmissions.update([tx.strip() for tx in t.split('\n')])
        elif t:
            transmissions.add(t)
    
    transmissions = sorted(transmissions)
    
    # Get price range for the form
    price_range = Car.objects.aggregate(min=models.Min('price'), max=models.Max('price'))
    
    context = {
        'cars': cars,
        'applied_filters': applied_filters,
        'body_types': body_types,
        'transmissions': transmissions,
        'price_range': price_range,
        'car_count': cars.count(),
    }
    
    return render(request, 'cars/search.html', context)

def car_detail(request, car_id):
    """
    View for displaying detailed information about a specific car.
    """
    car = get_object_or_404(Car, id=car_id)
    
    # Group car specifications into categories for better organization
    specs = {
        'basic_info': {
            'title': 'Basic Information',
            'items': [
                {'name': 'Make', 'value': car.make},
                {'name': 'Model', 'value': car.model},
                {'name': 'Year', 'value': car.year},
                {'name': 'Price', 'value': car.price, 'format': 'currency'},
            ]
        },
        'performance': {
            'title': 'Performance & Technical Specs',
            'items': [
                {'name': 'Engine', 'value': car.engine},
                {'name': 'Horsepower', 'value': car.horsepower},
                {'name': 'Transmission', 'value': car.transmission},
                {'name': 'Drivetrain', 'value': car.drivetrain},
                {'name': 'Fuel Economy (City)', 'value': car.fuel_economy_city, 'unit': 'km/L'},
                {'name': 'Fuel Economy (Highway)', 'value': car.fuel_economy_highway, 'unit': 'km/L'},
            ]
        },
        'dimensions': {
            'title': 'Dimensions & Capacity',
            'items': [
                {'name': 'Body Type', 'value': car.body_type},
                {'name': 'Seating Capacity', 'value': car.seats},
                {'name': 'Fuel Type', 'value': car.fuel_type},
                {'name': 'Wheel Size', 'value': car.wheel_size},
            ]
        },
        'features': {
            'title': 'Features',
            'items': [
                {'name': 'Safety Features', 'value': car.safety_features, 'format': 'list'},
                {'name': 'Technology Features', 'value': car.technology_features, 'format': 'list'},
                {'name': 'Interior Features', 'value': car.interior_features, 'format': 'list'},
                {'name': 'Warranty', 'value': car.warranty},
            ]
        }
    }
    
    # Find related cars (same body type or similar price range)
    related_cars = Car.objects.filter(
        models.Q(body_type=car.body_type) | 
        models.Q(price__range=(car.price * Decimal('0.8'), car.price * Decimal('1.2')))
    )
    context = {
        'car': car,
        'specs': specs,
        'related_cars': related_cars,
    }
    
    return render(request, 'cars/car_detail.html', context)