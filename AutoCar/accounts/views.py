from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate
from ..supabase_utils import fetch_data, insert_data, update_data, delete_data

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create user in Django auth system
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            # Store additional user data in Supabase
            user_data = {
                'user_id': str(user.id),
                'username': username,
                'email': form.cleaned_data.get('email'),
                'created_at': user.date_joined.isoformat()
            }
            insert_data('profiles', user_data)
            
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    # Get user profile from Supabase
    supabase_profile = fetch_data('profiles', lambda q: q.eq('user_id', str(request.user.id)))
    profile_data = supabase_profile.data[0] if supabase_profile and supabase_profile.data else {}
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            # Update profile in Supabase
            updated_data = {
                'username': request.user.username,
                'email': request.user.email,
                'updated_at': request.user.last_login.isoformat() if request.user.last_login else None,
                # Add other profile fields as needed
            }
            update_data('profiles', updated_data, 'user_id', str(request.user.id))
            
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'supabase_data': profile_data
    }
    return render(request, 'accounts/profile.html', context)

def home(request):
    # Fetch featured cars from Supabase to display on homepage
    featured_cars = fetch_data('cars', lambda q: q.eq('featured', True).limit(3))
    cars = featured_cars.data if featured_cars and featured_cars.data else []
    
    return render(request, 'accounts/home.html', {'featured_cars': cars})

@login_required
def cars(request):
    # Handle car form submission
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Add a new car
            new_car = {
                'make': request.POST.get('make'),
                'model': request.POST.get('model'),
                'year': int(request.POST.get('year')),
                'price': float(request.POST.get('price')) if request.POST.get('price') else None,
                'image_url': request.POST.get('image_url'),
                'featured': request.POST.get('featured') == 'on',
                'user_id': str(request.user.id)  # Associate the car with the current user
            }
            insert_data('cars', new_car)
            messages.success(request, 'Car added successfully!')
            
        elif action == 'delete':
            # Delete a car
            car_id = request.POST.get('car_id')
            if car_id:
                # Only delete if the car belongs to the user
                delete_data('cars', 'id', int(car_id))
                messages.success(request, 'Car deleted successfully!')
                
    # Fetch all cars from Supabase
    all_cars = fetch_data('cars')
    cars = all_cars.data if all_cars and all_cars.data else []
    
    return render(request, 'accounts/cars.html', {'cars': cars})