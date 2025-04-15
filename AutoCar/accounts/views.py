from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate
# Fix import path for supabase_utils
try:
    from AutoCar.utils.supabase_utils import fetch_data, insert_data, update_data, delete_data
except ImportError:
    try:
        from supabase_utils import fetch_data, insert_data, update_data, delete_data
    except ImportError:
        # Fallback functions to prevent crashes if imports fail
        def fetch_data(*args, **kwargs): 
            print(f"Mock fetch_data called with {args} {kwargs}")
            return type('obj', (object,), {'data': []})
        def insert_data(*args, **kwargs): 
            print(f"Mock insert_data called with {args} {kwargs}")
            return None
        def update_data(*args, **kwargs): 
            print(f"Mock update_data called with {args} {kwargs}")
            return None
        def delete_data(*args, **kwargs): 
            print(f"Mock delete_data called with {args} {kwargs}")
            return None

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
    profile_data = {}
    try:
        supabase_profile = fetch_data('profiles', lambda q: q.eq('user_id', str(request.user.id)))
        profile_data = supabase_profile.data[0] if supabase_profile and supabase_profile.data else {}
    except Exception as e:
        # Log the error
        print(f"Error fetching profile: {e}")
    
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
    cars = []  # Default empty list
    error_message = None
    
    try:
        featured_cars = fetch_data('cars', lambda q: q.eq('featured', True).limit(3))
        cars = featured_cars.data if featured_cars and featured_cars.data else []
    except Exception as e:
        # Handle error more gracefully
        error_message = str(e)
        print(f"Error fetching featured cars: {e}")
    
    context = {
        'featured_cars': cars,
        'error_message': error_message
    }
    
    return render(request, 'accounts/home.html', context)

# Add a dedicated error handler view
def error_handler(request):
    """
    View to display detailed error information for debugging
    """
    import sys
    import os
    import traceback
    from django.http import HttpResponse
    
    error_html = f"""
    <html>
    <head>
        <title>Diagnostic Information</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
            h1 {{ color: #333; }}
            h2 {{ color: #444; margin-top: 20px; }}
            pre {{ background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
            .section {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; }}
        </style>
    </head>
    <body>
        <h1>Diagnostic Information</h1>
        
        <div class="section">
            <h2>Python Information</h2>
            <p><strong>Python Version:</strong> {sys.version}</p>
            <p><strong>Python Path:</strong></p>
            <pre>{os.linesep.join(sys.path)}</pre>
        </div>
        
        <div class="section">
            <h2>Environment</h2>
            <p><strong>Current Directory:</strong> {os.getcwd()}</p>
            <p><strong>Directory Contents:</strong></p>
            <pre>{os.linesep.join(os.listdir())}</pre>
            <p><strong>Environment Variables:</strong></p>
            <pre>{os.linesep.join([f"{k}={'[REDACTED]' if k in ['SECRET_KEY', 'DATABASE_URL', 'SUPABASE_KEY'] else v}" for k, v in os.environ.items()])}</pre>
        </div>
        
        <div class="section">
            <h2>Import Test</h2>
            <pre>
import django: {check_import('django')}
import supabase_utils: {check_import('supabase_utils')}
import AutoCar.utils.supabase_utils: {check_import('AutoCar.utils.supabase_utils')}
from django.conf import settings: {check_import('django.conf.settings')}
            </pre>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(error_html)

def check_import(module_name):
    """Helper function to check if a module can be imported"""
    try:
        __import__(module_name)
        return "Success"
    except ImportError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@login_required
def cars(request):
    # Handle car form submission
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            try:
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
            except Exception as e:
                # Log the error
                print(f"Error adding car: {e}")
                messages.error(request, 'Error adding car. Please try again.')
            
        elif action == 'delete':
            try:
                # Delete a car
                car_id = request.POST.get('car_id')
                if car_id:
                    # Only delete if the car belongs to the user
                    delete_data('cars', 'id', int(car_id))
                    messages.success(request, 'Car deleted successfully!')
            except Exception as e:
                # Log the error
                print(f"Error deleting car: {e}")
                messages.error(request, 'Error deleting car. Please try again.')
                
    # Fetch all cars from Supabase
    cars = []
    try:
        all_cars = fetch_data('cars')
        cars = all_cars.data if all_cars and all_cars.data else []
    except Exception as e:
        # Log the error
        print(f"Error fetching cars: {e}")
    
    return render(request, 'accounts/cars.html', {'cars': cars})

def minimal_view(request):
    """
    A minimal view that doesn't use any database or complex features
    Just to test if basic template rendering works
    """
    try:
        return render(request, 'minimal.html')
    except Exception as e:
        return HttpResponse(f"Error in minimal view: {str(e)}", content_type="text/plain")