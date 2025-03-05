# AutoCar/recommendations/forms.py
from django import forms

class SurveyForm(forms.Form):
    age_choices = [
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('55+', '55+'),
    ]
    age = forms.ChoiceField(choices=age_choices)
    gender = forms.CharField(max_length=10)
    location = forms.CharField(max_length=100)
    occupation = forms.CharField(max_length=100)
    annual_income = forms.DecimalField(max_digits=10, decimal_places=2)
    years_of_driving_experience = forms.IntegerField()
    owns_car = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    current_car = forms.CharField(max_length=100)
    annual_miles = forms.IntegerField()
    owned_before = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    previous_cars = forms.CharField(widget=forms.Textarea)
    primary_purpose = forms.CharField(max_length=100)
    preferred_car_type = forms.CharField(max_length=100)
    preferred_car_brand = forms.CharField(max_length=100)
    budget = forms.DecimalField(max_digits=10, decimal_places=2)
    seating_capacity = forms.IntegerField()
    cargo_space = forms.CharField(max_length=100)
    preferred_fuel_type = forms.CharField(max_length=100)
    eco_friendly = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    transmission_type = forms.CharField(max_length=100)
    desired_fuel_efficiency = forms.CharField(max_length=100)
    preferred_drive_type = forms.CharField(max_length=100)
    advanced_technology = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    must_have_features = forms.CharField(widget=forms.Textarea)
    additional_info = forms.CharField(widget=forms.Textarea)