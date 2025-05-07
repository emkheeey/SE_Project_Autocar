from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
import logging
from AutoCar.utils.supabase_utils import fetch_data, insert_data, update_data, delete_data, get_supabase_client, ensure_bucket_exists, upload_file_to_storage
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import traceback
from django.conf import settings
import os

# Configure logging
logger = logging.getLogger(__name__)

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
                        logger.warning(f"Supabase error: {str(supabase_error)}")
                    
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
        logger.error(f"Error fetching profile: {e}")
    
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
        featured_cars = fetch_data('cars', lambda q: q.eq('featured', True).limit(6))
        if featured_cars and featured_cars.data:
            # Filter out variant cars - keep only parent models
            main_models = []
            for car in featured_cars.data:
                # Only include car if it doesn't have a parent_model_id
                # or doesn't have variant naming patterns
                if car.get('parent_model_id') is None and not any(
                    variant_word in car.get('model', '').lower() for variant_word in 
                    ['mt', 'at', 'cvt', 'dsl', 'diesel', 'cargo', 'j ', 'e ', 'g ', 'gr-s', 'xe', 'xle']):
                    main_models.append(car)
            
            # Only use filtered list if we have results, otherwise use original
            if main_models:
                cars = main_models
            else:
                cars = featured_cars.data
        else:
            cars = []
    except Exception as e:
        # Handle error more gracefully
        error_message = str(e)
        logger.error(f"Error fetching featured cars: {e}")
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
    try:
        # Fetch all cars first to have complete data available
        all_cars_result = fetch_data('cars')
        all_cars = all_cars_result.data if all_cars_result and all_cars_result.data else []
        
        logger.info(f"Total cars fetched from database: {len(all_cars)}")
        
        if not all_cars:
            logger.warning("No cars found in database")
            return render(request, 'accounts/cars.html', {'cars': []})
        
        # Multi-level filtering to ensure we only get parent models
        main_models = []
        
        # Step 1: First prioritize cars with featured=True (these should be main models)
        featured_cars = [car for car in all_cars if car.get('featured') == True]
        
        # Step 2: Also include cars with parent_model_id = null (these are also main models)
        null_parent_cars = [car for car in all_cars if car.get('parent_model_id') is None]
        
        # Combine both lists and remove duplicates by creating a dictionary keyed by car id
        combined_cars = {car['id']: car for car in featured_cars + null_parent_cars}
        
        # Step 3: Final filtering - remove any cars with variant-like names
        # More extensive list of variant indicators
        variant_indicators = [
            'mt', 'at', 'cvt', 'dsl', 'diesel', 'cargo', 'j mt', 'e mt', 'g mt', 
            'j at', 'e at', 'g at', 'gr-s', 'xe cvt', 'xle cvt', 'j cvt', 'e cvt',
            'zx at', 'gr sport', 'conquest', 'aluminum van'
        ]
        
        for car_id, car in combined_cars.items():
            model_name = car.get('model', '').lower()
            
            # Check if the model name contains any variant indicators
            if not any(indicator in model_name for indicator in variant_indicators):
                main_models.append(car)
                
        # If our filtering was too aggressive and removed all cars, use a fallback approach
        if not main_models and all_cars:
            logger.warning("Filtering removed all cars - using base models")
            # Extract just the base model name without variants, like "Camry", "Hilux", etc.
            # Group cars by their base model name and select one representative for each
            base_models = {}
            for car in all_cars:
                model_parts = car.get('model', '').split(' ')
                base_name = model_parts[0] if model_parts else ''
                
                # Only replace existing entry if current car is featured
                if base_name and (base_name not in base_models or car.get('featured')):
                    base_models[base_name] = car
            
            main_models = list(base_models.values())
                
        # Sort by model name
        main_models.sort(key=lambda x: x.get('model', ''))
        
        logger.info(f"Filtered main models count: {len(main_models)}")
        # Print first few car models to debug
        if main_models:
            for i, car in enumerate(main_models[:5]):
                logger.info(f"Car {i+1}: id={car.get('id')}, model={car.get('model')}")
        
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        main_models = []
    
    context = {
        'cars': main_models,
    }
    
    return render(request, 'accounts/cars.html', context)

def fetch_cars_data():
    """
    Fetch car data from Supabase including the additional fields for filtering
    """
    try:
        result = fetch_data('cars')
        if result and hasattr(result, 'data'):
            return result.data
        return []
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return []

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

def debug_car_info(request):
    """
    Debug view to display all car info for troubleshooting
    """
    try:
        # Fetch all cars
        all_cars_result = fetch_data('cars')
        all_cars = all_cars_result.data if all_cars_result and all_cars_result.data else []
        
        # Sort by model name for easier reading
        all_cars.sort(key=lambda x: x.get('model', ''))
        
        # Build HTML response
        response_text = f"""
        <html>
        <head>
            <title>Car Database Debug</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                th {{ background-color: #4CAF50; color: white; }}
                .highlight {{ background-color: #ffffcc; }}
                .parent {{ background-color: #d1e7dd; }}
                .variant {{ background-color: #f8d7da; }}
            </style>
        </head>
        <body>
            <h1>Car Database Debug Information</h1>
            <p>Total cars: {len(all_cars)}</p>
            
            <h2>All Cars</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Model</th>
                    <th>Parent ID</th>
                    <th>Featured</th>
                    <th>Image URL</th>
                </tr>
        """
        
        for car in all_cars:
            # Determine row class
            row_class = ''
            if car.get('parent_model_id') is None:
                row_class = 'parent'
            else:
                row_class = 'variant'
                
            response_text += f"""
                <tr class="{row_class}">
                    <td>{car.get('id')}</td>
                    <td>{car.get('model')}</td>
                    <td>{car.get('parent_model_id')}</td>
                    <td>{car.get('featured')}</td>
                    <td>{car.get('image_url', 'None')[:50]}{'...' if car.get('image_url') and len(car.get('image_url')) > 50 else ''}</td>
                </tr>
            """
            
        response_text += """
            </table>
            
            <h2>Car Variants Relationships</h2>
            <table>
                <tr>
                    <th>Parent Model</th>
                    <th>Parent ID</th>
                    <th>Variants</th>
                </tr>
        """
        
        # Group variants by parent
        parent_models = [car for car in all_cars if car.get('parent_model_id') is None]
        
        for parent in parent_models:
            parent_id = parent.get('id')
            variants = [car for car in all_cars if car.get('parent_model_id') == parent_id]
            
            variant_list = ", ".join([f"{v.get('model')} (ID: {v.get('id')})" for v in variants])
            
            response_text += f"""
                <tr>
                    <td>{parent.get('model')} (ID: {parent_id})</td>
                    <td>{parent_id}</td>
                    <td>{variant_list if variants else 'No variants'}</td>
                </tr>
            """
            
        response_text += """
            </table>
            
            <h2>Potential Issues</h2>
            <ul>
        """
        
        # Check for orphaned variants
        orphaned_variants = [car for car in all_cars if car.get('parent_model_id') and 
                           not any(p.get('id') == car.get('parent_model_id') for p in all_cars)]
        
        if orphaned_variants:
            response_text += f"<li>Found {len(orphaned_variants)} orphaned variants (parent ID doesn't exist)</li>"
            response_text += "<ul>"
            for v in orphaned_variants:
                response_text += f"<li>{v.get('model')} (ID: {v.get('id')}) references non-existent parent ID: {v.get('parent_model_id')}</li>"
            response_text += "</ul>"
        
        # Check for duplicate model names
        model_counts = {}
        for car in all_cars:
            model = car.get('model')
            if model in model_counts:
                model_counts[model] += 1
            else:
                model_counts[model] = 1
                
        duplicate_models = {model: count for model, count in model_counts.items() if count > 1}
        if duplicate_models:
            response_text += f"<li>Found {len(duplicate_models)} duplicate model names</li>"
            response_text += "<ul>"
            for model, count in duplicate_models.items():
                dupe_cars = [car for car in all_cars if car.get('model') == model]
                car_ids = [str(c.get('id')) for c in dupe_cars]
                response_text += f"<li>{model} appears {count} times: IDs: {', '.join(car_ids)}</li>"
            response_text += "</ul>"
            
        response_text += """
            </ul>
            
            <p><a href="/accounts/cars/">Back to Cars List</a></p>
        </body>
        </html>
        """
        
        return HttpResponse(response_text)
    except Exception as e:
        logger.error(f"Error in debug_car_info view: {e}")
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain")

@csrf_exempt
def update_car_image(request):
    if request.method == 'POST':
        try:
            # Extract all potential car ID sources
            form_car_id = request.POST.get('car_id')
            backup_car_id = request.POST.get('backup_car_id')
            
            # Log all incoming data for debugging
            logger.info(f"UPDATE CAR IMAGE REQUEST - POST DATA: {request.POST}")
            logger.info(f"Form car_id: {form_car_id}, Backup car_id: {backup_car_id}")
            
            # Step 1: Determine and validate the car ID - try all sources
            car_id = None
            
            # Try the form car_id first
            if form_car_id:
                try:
                    car_id = int(form_car_id)
                    logger.info(f"Using form car_id: {car_id}")
                except (ValueError, TypeError):
                    logger.warning(f"Invalid form car_id format: {form_car_id}")
            
            # If that failed, try backup_car_id
            if car_id is None and backup_car_id:
                try:
                    car_id = int(backup_car_id)
                    logger.info(f"Using backup car_id: {car_id}")
                except (ValueError, TypeError):
                    logger.warning(f"Invalid backup car_id format: {backup_car_id}")
            
            # If still no valid ID, try to parse from JSON body
            if car_id is None:
                try:
                    data = json.loads(request.body)
                    json_car_id = data.get('car_id')
                    if json_car_id:
                        car_id = int(json_car_id)
                        logger.info(f"Using JSON car_id: {car_id}")
                        
                        # If we also have an image URL in JSON, process direct URL update
                        image_url = data.get('image_url')
                        if image_url:
                            logger.info(f"Using direct URL update for car {car_id}: {image_url}")
                            
                            # Verify car exists
                            car_data = fetch_data('cars', lambda q: q.eq('id', car_id))
                            if not car_data or not car_data.data:
                                return JsonResponse({'error': f'Car with ID {car_id} not found'}, status=404)
                                
                            # Update image and return success
                            update_data('cars', {'image_url': image_url}, 'id', car_id)
                            return JsonResponse({
                                'success': True,
                                'image_url': image_url,
                                'car_id': car_id,
                                'car_model': car_data.data[0].get('model'),
                                'method': 'direct_url'
                            })
                except Exception as json_error:
                    logger.error(f"Error processing JSON data: {json_error}")
            
            # If we still don't have a valid car ID, return an error
            if car_id is None:
                logger.error("No valid car ID found in request")
                return JsonResponse({
                    'error': 'No valid car ID provided',
                    'request_data': {k: v for k, v in request.POST.items()}
                }, status=400)
            
            # Step 2: Verify car exists in database
            logger.info(f"Verifying car with ID {car_id} exists in database")
            car_data = fetch_data('cars', lambda q: q.eq('id', car_id))
            if not car_data or not car_data.data:
                logger.error(f"Car with ID {car_id} not found in database")
                return JsonResponse({
                    'error': f'Car with ID {car_id} not found in database',
                    'car_id': car_id
                }, status=404)
            
            # Extract car details
            car = car_data.data[0]
            car_model = car.get('model')
            parent_model_id = car.get('parent_model_id')
            logger.info(f"Found car: {car_model} (ID: {car_id}, Parent ID: {parent_model_id})")
            
            # Step 3: Process file upload
            if 'car_image' in request.FILES:
                image_file = request.FILES['car_image']
                logger.info(f"Processing file upload: {image_file.name}, size: {image_file.size}")
                
                # Upload to Supabase storage
                try:
                    # Generate unique filename
                    unique_filename = f"{uuid.uuid4()}_{image_file.name}"
                    
                    # Set up storage parameters
                    bucket_name = 'car-images'
                    file_path = f"{car_id}/{unique_filename}"
                    
                    # Read file content
                    file_content = image_file.read()
                    
                    # Attempt upload
                    success, result = upload_file_to_storage(
                        bucket_name, 
                        file_path, 
                        file_content, 
                        image_file.content_type
                    )
                    
                    if success:
                        image_url = result
                        logger.info(f"File uploaded successfully: {image_url}")
                        
                        # Update car record with new image URL
                        logger.info(f"Updating car record ID {car_id} with new image URL")
                        update_result = update_data('cars', {'image_url': image_url}, 'id', car_id)
                        
                        if update_result and hasattr(update_result, 'data'):
                            logger.info(f"Database updated: {len(update_result.data)} records")
                            
                            # Verify update worked
                            verify_result = fetch_data('cars', lambda q: q.eq('id', car_id))
                            if verify_result and verify_result.data:
                                current_url = verify_result.data[0].get('image_url')
                                logger.info(f"Verified new image URL: {current_url}")
                                
                            return JsonResponse({
                                'success': True,
                                'image_url': image_url,
                                'car_id': car_id,
                                'car_model': car_model
                            })
                        else:
                            logger.warning("Database update returned unexpected result")
                            return JsonResponse({
                                'error': 'Database update failed',
                                'car_id': car_id
                            }, status=500)
                    else:
                        logger.error(f"File upload failed: {result}")
                        return JsonResponse({
                            'error': f'File upload failed: {result}',
                            'car_id': car_id
                        }, status=500)
                except Exception as upload_error:
                    logger.error(f"Error during file upload: {upload_error}")
                    logger.error(traceback.format_exc())
                    return JsonResponse({
                        'error': f'Error during file upload: {str(upload_error)}',
                        'car_id': car_id
                    }, status=500)
            else:
                logger.error("No image file found in request")
                return JsonResponse({
                    'error': 'No image file uploaded',
                    'car_id': car_id
                }, status=400)
                
        except Exception as e:
            logger.error(f"Unhandled error in update_car_image: {e}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'error': f'Server error: {str(e)}',
                'detail': traceback.format_exc()
            }, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def debug_info(request):
    """
    Debug view to check environment and static file setup
    """
    data = {
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'STATICFILES_DIRS': [str(path) for path in settings.STATICFILES_DIRS],
        'STATICFILES_STORAGE': settings.STATICFILES_STORAGE,
        'DEBUG': settings.DEBUG,
        'BASE_DIR': str(settings.BASE_DIR),
        'static_files': []
    }
    
    # Check for static files
    try:
        static_root = settings.STATIC_ROOT
        if os.path.exists(static_root):
            data['static_root_exists'] = True
            # List some key static files
            for root, dirs, files in os.walk(static_root):
                for file in files:
                    if file.endswith('.css') or file.endswith('.js') or file.endswith('.png'):
                        rel_path = os.path.relpath(os.path.join(root, file), static_root)
                        data['static_files'].append(rel_path)
                        if len(data['static_files']) > 10:  # Limit to 10 files
                            break
        else:
            data['static_root_exists'] = False
    except Exception as e:
        data['static_files_error'] = str(e)
    
    # Current directory info
    try:
        data['cwd'] = os.getcwd()
        data['dir_contents'] = os.listdir()
    except Exception as e:
        data['dir_error'] = str(e)
        
    return JsonResponse(data)

# Add this debug view for static file testing
def debug_static(request):
    """
    View to test static file loading
    """
    from django.conf import settings
    
    context = {
        'STATIC_URL': settings.STATIC_URL,
        'DEBUG': settings.DEBUG,
        'request': request
    }
    return render(request, 'debug_static.html', context)

def car_detail(request, car_id):
    """
    View to display a car and its variants
    """
    try:
        # Fetch car details
        car_result = fetch_data('cars', lambda q: q.eq('id', car_id))
        if not car_result or not car_result.data:
            messages.error(request, "Car not found")
            return redirect('cars')
            
        car = car_result.data[0]
        
        # Fetch variants from the new car_variants table
        variants_result = fetch_data('car_variants', lambda q: q.eq('parent_model_id', car_id).order('price'))
        variants = variants_result.data if variants_result and variants_result.data else []
        
        # If no variants in new table, try the old approach as fallback
        if not variants:
            old_variants_result = fetch_data('cars', lambda q: q.eq('parent_model_id', car_id).order('price'))
            variants = old_variants_result.data if old_variants_result and old_variants_result.data else []
        
        context = {
            'car': car,
            'variants': variants,
        }
        
        return render(request, 'accounts/car_detail.html', context)
    except Exception as e:
        logger.error(f"Error in car_detail view: {e}")
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('cars')

def fix_variant_relationships(request):
    """
    Admin utility to ensure all variants are properly linked to their parent models.
    This should be run after importing new data or if variants are showing up on the main listing.
    """
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this function.")
        return redirect('home')
        
    try:
        # Get all cars
        all_cars_result = fetch_data('cars')
        all_cars = all_cars_result.data if all_cars_result and all_cars_result.data else []
        
        if not all_cars:
            messages.error(request, "No cars found in database.")
            return redirect('cars')
        
        # Step 1: First identify clear parent models
        parent_models = []
        variants = []
        
        # These are keywords that typically indicate a variant
        variant_indicators = [
            'mt', 'at', 'cvt', 'dsl', 'diesel', 'cargo', 'j mt', 'j at', 'e mt', 'e at', 'g mt', 'g at', 
            'gr-s', 'xe cvt', 'xle cvt', 'j cvt', 'e cvt', 'g cvt', 'zx at', 'gr sport', 'conquest', 
            'aluminum van', 'hev', 'turbo'
        ]
        
        # First pass - identify clear parents by featured flag and name
        for car in all_cars:
            model_name = car.get('model', '').lower()
            
            # Check if the model name contains any variant indicators
            is_variant = any(indicator in model_name for indicator in variant_indicators)
            
            # Main models should be featured and not have variant indicators in name
            if car.get('featured') and not is_variant:
                parent_models.append(car)
            # Everything else is a potential variant
            else:
                variants.append(car)
        
        # Step 2: For each variant, match to the correct parent model
        updates_count = 0
        for variant in variants:
            variant_name = variant.get('model', '')
            variant_id = variant.get('id')
            
            # Skip variants that already have correct parent_model_id
            if variant.get('parent_model_id') is not None:
                # Verify the parent exists
                parent_id = variant.get('parent_model_id')
                parent_exists = any(p.get('id') == parent_id for p in parent_models)
                
                if parent_exists:
                    continue
            
            # Extract the base model name from the variant name (e.g., "Hilux" from "Hilux 2.4 Cargo 4x2 MT")
            # We use the first word which typically is the base model name
            base_name = variant_name.split(' ')[0] if variant_name else ''
            
            if not base_name:
                continue
                
            # Find matching parent models
            matching_parents = [
                parent for parent in parent_models 
                if base_name.lower() in parent.get('model', '').lower()
            ]
            
            # If we found exact matches, use the first one
            if matching_parents:
                matching_parent = matching_parents[0]
                # Update the variant to link to this parent
                update_data('cars', {'parent_model_id': matching_parent.get('id')}, 'id', variant_id)
                updates_count += 1
            else:
                # No exact match found - try to create a simple matching algorithm based on name
                for parent in parent_models:
                    parent_name = parent.get('model', '').lower()
                    # Check if parent name is contained in variant name (usually true)
                    if parent_name in variant_name.lower():
                        update_data('cars', {'parent_model_id': parent.get('id')}, 'id', variant_id)
                        updates_count += 1
                        break
        
        # Step 3: If no parent models were found, create them from the variants
        if not parent_models and variants:
            # Group variants by base model name
            model_groups = {}
            for variant in variants:
                variant_name = variant.get('model', '')
                base_name = variant_name.split(' ')[0] if variant_name else ''
                
                if base_name:
                    if base_name not in model_groups:
                        model_groups[base_name] = []
                    model_groups[base_name].append(variant)
            
            # For each group, select one to be the parent (the simplest named one)
            for base_name, group in model_groups.items():
                if not group:
                    continue
                    
                # Sort by name length - shorter names are likely simpler base models
                group.sort(key=lambda x: len(x.get('model', '')))
                parent_candidate = group[0]
                
                # Update this variant to be a parent model
                update_data('cars', {'featured': True, 'parent_model_id': None}, 'id', parent_candidate.get('id'))
                
                # Update all other variants in the group to link to this parent
                for variant in group[1:]:
                    if variant.get('id') != parent_candidate.get('id'):
                        update_data('cars', {'parent_model_id': parent_candidate.get('id')}, 'id', variant.get('id'))
                        updates_count += 1
        
        messages.success(request, f"Updated {updates_count} variants with correct parent model relationships.")
    except Exception as e:
        logger.error(f"Error fixing variant relationships: {e}")
        messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect('cars')

def debug_car_detail(request, car_id):
    """
    Debug version of the car detail view to test direct access
    """
    try:
        # Fetch car details
        car_result = fetch_data('cars', lambda q: q.eq('id', car_id))
        if not car_result or not car_result.data:
            return HttpResponse(f"Car with ID {car_id} not found", content_type="text/plain")
            
        car = car_result.data[0]
        
        # Fetch variants from the new car_variants table
        variants_result = fetch_data('car_variants', lambda q: q.eq('parent_model_id', car_id))
        variants = variants_result.data if variants_result and variants_result.data else []
        
        # If no variants in new table, try the old approach as fallback
        if not variants:
            old_variants_result = fetch_data('cars', lambda q: q.eq('parent_model_id', car_id))
            variants = old_variants_result.data if old_variants_result and old_variants_result.data else []
        
        # Debug output
        response_text = f"""
        <html>
        <head><title>Debug Car Detail</title></head>
        <body>
            <h1>Car Detail Debug View</h1>
            <h2>Car: {car.get('model')} (ID: {car.get('id')})</h2>
            <p>Year: {car.get('year')}</p>
            <p>Price: {car.get('price')}</p>
            <p>Body Type: {car.get('body_type')}</p>
            
            <h3>Found {len(variants)} variants:</h3>
            <ul>
        """
        
        for variant in variants:
            response_text += f"<li>{variant.get('model')} (ID: {variant.get('id')}) - Price: {variant.get('price')}</li>"
        
        response_text += """
            </ul>
            
            <p><a href="/cars/">Back to Cars List</a></p>
        </body>
        </html>
        """
        
        return HttpResponse(response_text)
    except Exception as e:
        logger.error(f"Error in debug_car_detail view: {e}")
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain")

def car_variants_json(request, car_id):
    """
    JSON API endpoint to return variants for a car
    """
    try:
        # Debug log for tracking
        logger.info(f"Fetching variants for parent car ID: {car_id}")
        
        # Fetch variants from the new car_variants table
        variants_result = fetch_data('car_variants', lambda q: q.eq('parent_model_id', car_id))
        variants = variants_result.data if variants_result and variants_result.data else []
        
        # If no variants in new table, try the old approach as fallback
        if not variants:
            old_variants_result = fetch_data('cars', lambda q: q.eq('parent_model_id', car_id))
            variants = old_variants_result.data if old_variants_result and old_variants_result.data else []
            logger.info(f"Found {len(variants)} variants using old approach")
        else:
            logger.info(f"Found {len(variants)} variants in car_variants table")
        
        # Comprehensive variant ID mapping based on model names
        # This mapping ensures all variant IDs match those in the CSV file
        variant_id_map = {
            # Toyota Alphard variants
            "Alphard 2.5 HEV CVT": 30,
            
            # Toyota Avanza variants
            "Avanza 1.3 E CVT": 31,
            "Avanza 1.3 E M/T": 32,
            "Avanza 1.3 J M/T": 33,
            "Avanza 1.5 G CVT": 34,
            
            # Toyota Camry variants
            "Camry Hybrid 2.5 HEV": 35,
            "Camry Hybrid 2.5 HEV White Pearl Mica": 36,
            
            # Toyota Coaster variants
            "Coaster 29-Seater": 37,
            
            # Toyota GR Yaris variants
            "GR Yaris 1.6 Turbo MT": 38,
            "GR Yaris 1.6 Turbo MT (Emotional Red)": 39,
            
            # Toyota Corolla Altis variants
            "Corolla Altis 1.8 E CVT": 40,
            "Corolla Altis 1.8 G GR-S CVT": 41,
            "Corolla Altis 1.8 GR-S Hybrid CVT": 42,
            
            # Toyota Fortuner variants
            "Fortuner 2.4 G Diesel 4x2 AT": 43,
            "Fortuner 2.4 G Diesel 4x2 MT": 44,
            
            # Toyota GR Supra variants
            "GR Supra 3.0 Turbo Inline-6 AT (Black Metallic 2)": 45,
            
            # Toyota GR86 variants
            "GR86 2.4 AT": 46,
            "GR86 2.4 MT": 47,
            
            # Toyota Hiace variants
            "Hiace 2.8 Commuter Deluxe MT": 48,
            "Hiace 2.8 GL Grandia AT": 49,
            "Hiace 3.0 Ambulance": 50,
            "Hiace 3.0 Cargo": 51,
            
            # Toyota Hilux variants
            "Hilux 2.4 Cab & Chassis 4x2 MT": 52,
            "Hilux 2.4 Cargo 4x2 MT": 53,
            "Hilux 2.4 E DSL 4x2 AT": 54,
            "Hilux 2.8 GR Sport AT": 55,
            "Hilux Conquest 2.4 DSL": 56,
            
            # Toyota Innova variants
            "Innova 2.8 E Diesel AT": 57,
            
            # Toyota Land Cruiser variants
            "Land Cruiser ZX AT (Precious White Pearl)": 59,
            
            # Toyota Vios variants
            "Vios 1.3 J MT": 61,
            "Vios 1.3 XE CVT": 62,
            "Vios 1.3 XLE CVT": 63,
            
            # Toyota Wigo variants
            "Wigo 1.0 E CVT": 64,
            "Wigo 1.0 J MT": 65
        }
        
        # Parent model correction map - fixed parent relationships
        # This ensures variants are associated with the correct parent models 
        parent_model_correction = {
            # Fix GR Yaris variants to show under GR Yaris (not GR Supra)
            38: 20,  # GR Yaris 1.6 Turbo MT belongs to GR Yaris (ID 20)
            39: 20,  # GR Yaris 1.6 Turbo MT (Emotional Red) belongs to GR Yaris (ID 20)
            
            # Additional parent corrections if needed
            # variant_id: correct_parent_id,
        }
        
        # If we're looking for GR Supra variants (car_id = 19) but getting GR Yaris variants
        # Filter out the incorrectly associated variants
        if car_id == 19:  # GR Supra parent ID
            # Log that we're fixing the issue
            logger.info("GR Supra selected - filtering out incorrect GR Yaris variants")
            
            # Log all variants before filtering for debugging
            logger.info(f"Before filtering - variants count: {len(variants)}")
            for v in variants:
                logger.info(f"Before filtering - variant ID: {v.get('id')}, Model: {v.get('model')}")
            
            # Identify the specific variants to remove (GR Yaris variants)
            yaris_variant_ids = [38, 39]
            
            # Filter to keep only true GR Supra variants (exclude only IDs 38 and 39)
            original_count = len(variants)
            variants = [v for v in variants if v.get('id') not in yaris_variant_ids]
            filtered_count = len(variants)
            
            logger.info(f"Filtered out {original_count - filtered_count} GR Yaris variants from GR Supra")
            
            # Also look for the correct GR Supra variant (ID 45)
            supra_variant_result = fetch_data('cars', lambda q: q.eq('id', 45))
            if supra_variant_result and supra_variant_result.data:
                # Add it if it wasn't already included
                supra_variant = supra_variant_result.data[0]
                if not any(v.get('id') == 45 for v in variants):
                    variants.append(supra_variant)
                    logger.info("Added correct GR Supra variant (ID 45)")
            
            # Log variants after filtering
            logger.info(f"After filtering - variants count: {len(variants)}")
            for v in variants:
                logger.info(f"After filtering - variant ID: {v.get('id')}, Model: {v.get('model')}")
        
        # If we're looking for GR Yaris variants (car_id = 20)
        # Make sure we include the GR Yaris variants even if they're incorrectly associated
        elif car_id == 20:  # GR Yaris parent ID
            # Log that we're fixing the issue
            logger.info("GR Yaris selected - ensuring GR Yaris variants are included")
            
            # Look for GR Yaris variants directly by ID
            for yaris_variant_id in [38, 39]:
                # Check if this variant is already included
                if not any(v.get('id') == yaris_variant_id for v in variants):
                    # Fetch the variant directly by ID
                    yaris_variant_result = fetch_data('cars', lambda q: q.eq('id', yaris_variant_id))
                    if yaris_variant_result and yaris_variant_result.data:
                        variants.append(yaris_variant_result.data[0])
                        logger.info(f"Added GR Yaris variant (ID {yaris_variant_id})")
            
            # Force parent_model_id to be correct for all variants
            for variant in variants:
                variant['parent_model_id'] = 20  # Ensure everything shows under GR Yaris
                logger.info(f"Set parent_model_id to 20 for variant {variant.get('id')}")
            
            # Log final variants
            logger.info(f"Final variants count for GR Yaris: {len(variants)}")
            for v in variants:
                logger.info(f"GR Yaris variant: ID={v.get('id')}, Model={v.get('model')}, Parent={v.get('parent_model_id')}")
        
        # Log all variant details for debugging
        for index, variant in enumerate(variants):
            variant_model = variant.get('model')
            original_id = variant.get('id')
            
            # Apply ID correction from the mapping
            if variant_model in variant_id_map:
                corrected_id = variant_id_map[variant_model]
                if original_id != corrected_id:
                    logger.info(f"CORRECTING ID for '{variant_model}': {original_id} -> {corrected_id}")
                    variant['id'] = corrected_id
            
            # Also, override parent model ID if needed based on the correction map
            if original_id in parent_model_correction:
                variant['parent_model_id'] = parent_model_correction[original_id]
                logger.info(f"CORRECTING PARENT for variant ID {original_id}: Parent set to {parent_model_correction[original_id]}")
            
            logger.info(f"Variant {index+1}: ID={variant.get('id')}, Model={variant_model}, Parent={variant.get('parent_model_id')}")
        
        # Format variant prices for display
        for variant in variants:
            if 'price' in variant:
                try:
                    variant['price'] = '{:,.2f}'.format(float(variant['price']))
                except (ValueError, TypeError):
                    pass
        
        return JsonResponse({
            'success': True,
            'variants': variants
        })
    except Exception as e:
        logger.error(f"Error fetching variants: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
