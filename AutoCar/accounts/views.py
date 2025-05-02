from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout

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
        try:
            form = SignUpForm(request.POST)
            if form.is_valid():
                # Create user in Django auth system
                try:
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    email = form.cleaned_data.get('email')
                    raw_password = form.cleaned_data.get('password1')
                                        
                    # Set first_name and last_name on User model
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    
                    # Authentication attempt
                    try:
                        user = authenticate(username=username, password=raw_password)
                        if user is not None:
                            login(request, user)
                        else:
                            messages.error(request, "Authentication failed after user creation")
                    except Exception as auth_error:
                        messages.error(request, f"Authentication error: {str(auth_error)}")
                    
                    # Store additional user data in Supabase - make this optional
                    try:
                        user_data = {
                            'user_id': str(user.id),
                            'username': username,
                            'email': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'created_at': user.date_joined.isoformat()
                        }
                        insert_data('profiles', user_data)
                    except Exception as supabase_error:
                        # Don't fail if Supabase storage fails - just log the error
                        messages.warning(request, f"Note: User profile sync to database failed, but your account was created.")
                        print(f"Supabase error: {str(supabase_error)}")
                    
                    messages.success(request, f'Account created for {username}!')
                    return redirect('home')
                except Exception as user_save_error:
                    messages.error(request, f"Error creating user: {str(user_save_error)}")
            else:
                # Form validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as outer_error:
            messages.error(request, f"Unexpected error: {str(outer_error)}")
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
        
        favorites = []
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'supabase_data': profile_data,
        'favorites': favorites,
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
        messages.warning(request, "Unable to fetch featured cars. Using demo data instead.")
        # Provide demo data if database fetch fails
        cars = [
            {
                'id': 1, 
                'make': 'Toyota', 
                'model': 'Camry', 
                'year': 2023, 
                'price': 25000.00,
                'image_url': 'https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2'
            },
            {
                'id': 2, 
                'make': 'Honda', 
                'model': 'Accord', 
                'year': 2023, 
                'price': 27000.00,
                'image_url': 'https://images.unsplash.com/photo-1583121274602-3e2820c69888'
            },
            {
                'id': 3, 
                'make': 'Tesla', 
                'model': 'Model 3', 
                'year': 2023, 
                'price': 42000.00,
                'image_url': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89'
            }
        ]
    
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
    """
    View to browse all cars with filtering capabilities
    """
    # Fetch all cars from your database
    # Make sure to include body_type and transmission fields
    cars_data = fetch_cars_data()
    
    context = {
        'cars': cars_data,
    }
    
    return render(request, 'accounts/cars.html', context)

def fetch_cars_data():
    """
    Fetch car data from Supabase including the additional fields for filtering
    """
    # Implement your Supabase fetching logic here
    # Make sure to include body_type, transmission and price fields needed for filtering
    
    # Your existing fetch code...
    # ...
    
    #return cars_list

def minimal_view(request):
    """
    A minimal view that doesn't use any database or complex features
    Just to test if basic template rendering works
    """
    try:
        return render(request, 'minimal.html')
    except Exception as e:
        return HttpResponse(f"Error in minimal view: {str(e)}", content_type="text/plain")
    
def about_view(request):
    return render(request, 'accounts/about.html')

def logout_view(request):
    """Custom logout view that redirects to the base page."""
    if request.method == 'POST':
        # Log the user out
        logout(request)
        
        # Add a success message (optional)
        messages.success(request, "You have been successfully logged out.")
        
        # Redirect to the base page (root URL)
        return redirect('base')
    
    # If not a POST request, redirect to home page
    return redirect('base')

def base_view(request):
    """View that renders the base template directly."""
    context = {}
    
    # You may want to include any context data that base.html needs
    if not request.user.is_authenticated:
        # Maybe add a message for logged out users
        messages.info(request, "You have been logged out. Please login to continue.")
    
    return render(request, 'base.html', context)
