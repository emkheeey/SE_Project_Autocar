import json
import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
       if request.method == 'POST':
           form = UserCreationForm(request.POST)
           if form.is_valid():
               user = form.save()
               login(request, user)  # Log the user in after registration
               return redirect('login')  # Redirect to the login page after registration
       else:
           form = UserCreationForm()
       return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
       if request.method == 'POST':
           form = UserUpdateForm(request.POST, instance=request.user)
           if form.is_valid():
               form.save()
               return redirect('profile')  # Redirect to the profile page
       else:
           form = UserUpdateForm(instance=request.user)
           return render(request, 'accounts/profile.html', {'form': form})
       
def user_login(request):
       if request.method == 'POST':
           form = AuthenticationForm(data=request.POST)
           if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               user = authenticate(username=username, password=password)
               if user is not None:
                   login(request, user)
                   return redirect('home')  # Redirect to the profile page
       else:
           form = AuthenticationForm()
       return render(request, 'accounts/login.html', {'form': form})
   
def home_view(request):
       return render(request, 'accounts/home.html')  # Ensure this path is correct


def browse_view(request):
    # Path to your JSON file
    json_file_path = os.path.join(settings.STATIC_ROOT, 'data', 'toyota_cars_data.json')
    
    try:
        with open(json_file_path, 'r') as file:
            cars_data = json.load(file)
            
        # Transform the JSON data into the format needed for the template
        cars = []
        for car in cars_data:
            # Create a car dictionary with the required fields
            car_type = car.get('body_type', 'Sedan')  # Default to 'None' if not specified
            car_dict = {
                'id': car['model'].lower().replace(' ', '_'),
                'name': car['model'].upper(),
                'image': f"{car['model'].lower().replace(' ', '_')}.jpg", 
                'price': car['price'],
                'type': car['specs']['body_type'].split('\n')[0], #Sedan
                'specs': car['specs']
            }
            cars.append(car_dict)
            
    except FileNotFoundError:
        # Fallback to hardcoded list f JSON file is not found
        cars = [
            {'id': 'alphard', 'name': 'ALPHARD', 'image': 'alphard.jpg', 'price': 4671000.0, 'type': 'MPV'},
            {'id': 'avanza', 'name': 'AVANZA', 'image': 'avanza.jpg', 'price': 844000.0, 'type': 'MPV'},
            {'id': 'camry', 'name': 'CAMRY', 'image': 'camry.jpg', 'price': 2657000.0, 'type': 'Sedan'},
            {'id': 'coaster', 'name': 'COASTER', 'image': 'coaster.jpg', 'price': 4114000.0, 'type': 'Commercial'},
            {'id': 'corolla_altis', 'name': 'COROLLA ALTIS', 'image': 'corolla_altis.jpg', 'price': 1213000.0, 'type': 'Sedan'},
            {'id': 'corolla_cross', 'name': 'COROLLA CROSS', 'image': 'corolla_cross.jpg', 'price': 1514000.0, 'type': 'SUV'},
            {'id': 'fortuner', 'name': 'FORTUNER', 'image': 'fortuner.jpg', 'price': 1775000.0, 'type': 'SUV'},
            {'id': 'gr_supra', 'name': 'GR SUPRA', 'image': 'gr_supra.jpg', 'price': 5552000.0, 'type': 'Sports'},
            {'id': 'gr_yaris', 'name': 'GR YARIS', 'image': 'gr_yaris.jpg', 'price': 3391000.0, 'type': 'Sports'},
            {'id': 'gr86', 'name': 'GR86', 'image': 'gr86.jpg', 'price': 2716000.0, 'type': 'Sports'},
            {'id': 'hiace', 'name': 'HIACE', 'image': 'hiace.jpg', 'price': 1195000.0, 'type': 'Commercial'},
            {'id': 'hiace_super_grandia', 'name': 'HIACE SUPER GRANDIA', 'image': 'hiace_super_grandia.jpg', 'price': 2906000.0, 'type': 'Commercial'},
            {'id': 'hilux', 'name': 'HILUX', 'image': 'hilux.jpg', 'price': 891000.0, 'type': 'Commercial'},
            {'id': 'innova', 'name': 'INNOVA', 'image': 'innova.jpg', 'price': 1267000.0, 'type': 'MPV'},
            {'id': 'land_cruiser', 'name': 'LAND CRUISER', 'image': 'land_cruiser.jpg', 'price': 5758000.0, 'type': 'SUV'},
            {'id': 'land_cruiser_prado', 'name': 'LAND CRUISER PRADO', 'image': 'land_cruiser_prado.jpg', 'price': 4806000.0, 'type': 'SUV'},
            {'id': 'lite_ace', 'name': 'LITE ACE', 'image': 'lite_ace.jpg', 'price': 651000.0, 'type': 'Commercial'},
            {'id': 'raize', 'name': 'RAIZE', 'image': 'raize.jpg', 'price': 757000.0, 'type': 'SUV'},
            {'id': 'rav4', 'name': 'RAV4', 'image': 'rav4.jpg', 'price': 2052000.0, 'type': 'SUV'},
            {'id': 'rush', 'name': 'RUSH', 'image': 'rush.jpg', 'price': 1208000.0, 'type': 'SUV'},
            {'id': 'tamaraw', 'name': 'TAMARAW', 'image': 'tamaraw.jpg', 'price': 757000.0, 'type': 'Commercial'},
            {'id': 'veloz', 'name': 'VELOZ', 'image': 'veloz.jpg', 'price': 1104000.0, 'type': 'MPV'},
            {'id': 'vios', 'name': 'VIOS', 'image': 'vios.jpg', 'price': 738000.0, 'type': 'Sedan'},
            {'id': 'wigo', 'name': 'WIGO', 'image': 'wigo.jpg', 'price': 615000.0, 'type': 'Hatchback'},
            {'id': 'yaris_cross', 'name': 'YARIS CROSS', 'image': 'yaris_cross.jpg', 'price': 1210000.0, 'type': 'SUV'},
            {'id': 'zenix', 'name': 'ZENIX', 'image': 'zenix.jpg', 'price': 1676000.0, 'type': 'MPV'}
        ]
    
    return render(request, 'accounts/browse.html', {'cars': cars})