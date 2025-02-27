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
                   return redirect('profile')  # Redirect to the profile page
       else:
           form = AuthenticationForm()
       return render(request, 'accounts/login.html', {'form': form})