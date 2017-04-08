from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Renders the home page with the correct data for the current user
from django.shortcuts import render

from HealthApp import staticHelpers
from HealthApp.models import Patient


def render_view(request, user_type, user):
    patients = staticHelpers.find_patients(user_type, user)
    all_patients = Patient.objects.all()

    if user_type == staticHelpers.UserTypes.patient:
        return redirect('/')
    elif user_type == staticHelpers.UserTypes.doctor:
        return render(request, 'HealthApp/all_patients.html',
                      {'user_type': user_type, 'patients': patients, 'all_patients': all_patients})
    elif user_type == staticHelpers.UserTypes.nurse:
        return render(request, 'HealthApp/all_patients.html',
                      {'user_type': user_type, 'patients': patients})


# Called when the home view is loaded or a form is submitted
@login_required(login_url="login/")
def all_patients(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')
    else:
        return render_view(request, user_type, user)