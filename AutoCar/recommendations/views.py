# AutoCar/recommendations/views.py
from django.shortcuts import render, redirect
from .forms import SurveyForm  # Import the SurveyForm
from .models import SurveyResponse  # Import the SurveyResponse model

def survey_view(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Process the form data and save it to the database
            survey_response = SurveyResponse(
                age=form.cleaned_data['age'],  # Should be a string like '25-34'
                gender=form.cleaned_data['gender'],  # Ensure this is a valid string
                location=form.cleaned_data['location'],  # Ensure this is a valid string
                occupation=form.cleaned_data['occupation'],  # Ensure this is a valid string
                annual_income=form.cleaned_data['annual_income'],  # Should be a decimal
                years_of_driving_experience=form.cleaned_data['years_of_driving_experience'],  # Should be an integer
                owns_car=form.cleaned_data['owns_car'] == 'Yes',  # Ensure this is a boolean
                current_car=form.cleaned_data['current_car'],  # Ensure this is a valid string
                annual_miles=form.cleaned_data['annual_miles'],  # Should be an integer
                owned_before=form.cleaned_data['owned_before'] == 'Yes',  # Ensure this is a boolean
                previous_cars=form.cleaned_data['previous_cars'],  # Ensure this is a valid string
                primary_purpose=form.cleaned_data['primary_purpose'],  # Ensure this is a valid string
                preferred_car_type=form.cleaned_data['preferred_car_type'],  # Ensure this is a valid string
                preferred_car_brand=form.cleaned_data['preferred_car_brand'],  # Ensure this is a valid string
                budget=form.cleaned_data['budget'],  # Should be a decimal
                seating_capacity=form.cleaned_data['seating_capacity'],  # Should be an integer
                cargo_space=form.cleaned_data['cargo_space'],  # Ensure this is a valid string
                preferred_fuel_type=form.cleaned_data['preferred_fuel_type'],  # Ensure this is a valid string
                eco_friendly=form.cleaned_data['eco_friendly'] == 'Yes',  # Ensure this is a boolean
                transmission_type=form.cleaned_data['transmission_type'],  # Ensure this is a valid string
                desired_fuel_efficiency=form.cleaned_data['desired_fuel_efficiency'],  # Ensure this is a valid string
                preferred_drive_type=form.cleaned_data['preferred_drive_type'],  # Ensure this is a valid string
                advanced_technology=form.cleaned_data['advanced_technology'] == 'Yes',  # Ensure this is a boolean
                must_have_features=form.cleaned_data['must_have_features'],  # Ensure this is a valid string
                additional_info=form.cleaned_data['additional_info'],  # Ensure this is a valid string
            )
            survey_response.save()  # Save the response to the database
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = SurveyForm()

    return render(request, 'survey/survey.html', {'form': form})  # Render the survey form
def success_view(request):
       return render(request, 'survey/success.html')  # Render the success page