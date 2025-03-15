from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=100, default="Toyota")
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Technical specs
    engine = models.CharField(max_length=100, null=True, blank=True)
    horsepower = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=100, null=True, blank=True)
    fuel_economy_city = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fuel_economy_highway = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    # Additional specs from AutoDeal
    body_type = models.CharField(max_length=100, null=True, blank=True)
    seats = models.CharField(max_length=50, null=True, blank=True)
    fuel_type = models.CharField(max_length=100, null=True, blank=True)
    drivetrain = models.CharField(max_length=100, null=True, blank=True)
    wheel_size = models.CharField(max_length=50, null=True, blank=True)
    warranty = models.CharField(max_length=100, null=True, blank=True)
    
    # Features
    interior_features = models.TextField(null=True, blank=True)
    safety_features = models.TextField(null=True, blank=True)
    technology_features = models.TextField(null=True, blank=True)
    
    # Media
    image_url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"