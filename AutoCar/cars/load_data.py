import json
from cars.models import Car

def load_cars_from_json(json_path):
    """Load scraped car data from JSON into the database"""
    with open(json_path, 'r', encoding='utf-8') as f:
        cars_data = json.load(f)
    
    count = 0
    for car_data in cars_data:
        try:
            # Extract basic car info
            make = car_data.get('make', 'Toyota')
            model = car_data.get('model', '')
            year = car_data.get('year', 2025)
            price = car_data.get('price')
            image_url = car_data.get('image_url')
            
            # Extract specs
            specs = car_data.get('specs', {})
            
            # Create or update car in database
            car, created = Car.objects.update_or_create(
                make=make,
                model=model,
                year=year,
                defaults={
                    'price': price,
                    'engine': specs.get('max_output'),
                    'horsepower': specs.get('horsepower'),
                    'transmission': specs.get('transmission'),
                    'body_type': specs.get('body_type'),
                    'seats': specs.get('seats'),
                    'fuel_type': specs.get('fuel_type'),
                    'drivetrain': specs.get('drivetrain'),
                    'wheel_size': specs.get('wheel_size'),
                    'warranty': specs.get('warranty'),
                    'image_url': image_url,
                    'safety_features': f"Airbags: {specs.get('airbags')}, ISOFIX: {specs.get('isofix')}, Front Parking Sensors: {specs.get('front_parking_sensors')}, Rear Parking Sensors: {specs.get('rear_parking_sensors')}",
                    'technology_features': specs.get('connectivity'),
                }
            )
            count += 1
        except Exception as e:
            print(f"Error loading {car_data.get('model', 'unknown')}: {e}")
    
    return count