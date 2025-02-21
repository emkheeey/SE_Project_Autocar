from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page (to be created later)
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# Register View
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    
    return render(request, 'accounts/register.html')

from django.shortcuts import render

def home(request):
    return render(request, "accounts/home.html")  # Keep this as is
