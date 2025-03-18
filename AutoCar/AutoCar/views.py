from django.shortcuts import render

def landing_page(request):
       return render(request, 'landingpage.html')

def about_view(request):
    return render(request, 'accounts/about.html')