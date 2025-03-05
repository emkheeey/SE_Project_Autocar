# AutoCar/recommendations/models.py
from django.db import models

class SurveyResponse(models.Model):
    age = models.CharField(max_length=10)  # This is fine for age ranges like '25-34'
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    years_of_driving_experience = models.IntegerField()
    owns_car = models.BooleanField()
    current_car = models.CharField(max_length=100)
    annual_miles = models.IntegerField()
    owned_before = models.BooleanField()
    previous_cars = models.TextField()
    primary_purpose = models.CharField(max_length=100)
    preferred_car_type = models.CharField(max_length=100)
    preferred_car_brand = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    seating_capacity = models.IntegerField()
    cargo_space = models.CharField(max_length=100)
    preferred_fuel_type = models.CharField(max_length=100)
    eco_friendly = models.BooleanField()
    transmission_type = models.CharField(max_length=100)
    desired_fuel_efficiency = models.CharField(max_length=100)
    preferred_drive_type = models.CharField(max_length=100)
    advanced_technology = models.BooleanField()
    must_have_features = models.TextField()
    additional_info = models.TextField()

    def __str__(self):
        return f"SurveyResponse by {self.gender}, Age: {self.age}"