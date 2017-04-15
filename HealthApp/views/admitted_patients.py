from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Renders the home page with the correct data for the current user
from django.shortcuts import render

from HealthApp import staticHelpers
from HealthApp.forms import SetPatientHospital
from HealthApp.forms.send_message import SendMessage
from HealthApp.models import Patient, AdmissionLog
from django.template.defaulttags import register


def render_view(request, user_type, user):
    admitted_patients = staticHelpers.get_admitted_patients()
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

    if user_type == staticHelpers.UserTypes.patient:
        return redirect('/')
    elif user_type == staticHelpers.UserTypes.doctor:
        setPatientHospitalForms = dict()
        for patient in admitted_patients:
            setPatientHospitalForms[patient.username] = SetPatientHospital(patient)
        return render(request, 'HealthApp/admitted_patients.html',
                      {'user_type': user_type, 'admitted_patients': admitted_patients,
                       'setPatientHospitalForms': setPatientHospitalForms, 'unread_messages': unread_messages, 'sendMessage': sendMessage})
    elif user_type == staticHelpers.UserTypes.nurse:
        return render(request, 'HealthApp/admitted_patients.html',
                      {'user_type': user_type, 'admitted_patients': admitted_patients, 'unread_messages': unread_messages, 'sendMessage': sendMessage})

    @register.filter(name='get_item')
    def get_item(dictionary, key):
        return dictionary.get(key)  # Called when the home view is loaded or a form is submitted


# Called when the home view is loaded or a form is submitted
@login_required(login_url="login/")
def admitted_patients(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')
    else:
        return render_view(request, user_type, user)
