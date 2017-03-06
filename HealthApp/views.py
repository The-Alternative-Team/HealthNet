from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import Register, Login, SelectAppointment, AddAppointment
from HealthApp import StaticHelpers
from .models import Patient, Doctor, Appointment


@login_required(login_url="login/")
def home(request):
    user_type, user = StaticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real-user only data
    if user_type == StaticHelpers.UserTypes.admin:
        return redirect('/admin/')

    if request.method == 'POST':
        # A form was submitted

        # TODO: Figure out which form instead of assuming it was the new appointment form

        # Get appointment_doctor
        if user_type == StaticHelpers.UserTypes.nurse:
            doctor_id = int(request.POST['doctor'])
            appointment_doctor = Doctor.objects.all().filter(id=doctor_id)[0]
        elif user_type == StaticHelpers.UserTypes.doctor:
            appointment_doctor = user
        else:
            # It's a patient
            appointment_doctor = user.primary_doctor

        # Get appointment_patient
        if user_type == StaticHelpers.UserTypes.patient:
            appointment_patient = user
        else:
            patient_id = int(request.POST['patient'])
            appointment_patient = Patient.objects.all().filter(id=patient_id)[0]

        appointment = Appointment(hospital=appointment_patient.hospital, doctor=appointment_doctor,
                                  patient=appointment_patient, start_time=request.POST['start_time'],
                                  end_time=request.POST['end_time'], notes=request.POST['notes'])
        appointment.save()

        # Redirect as a GET so refreshing works
        return redirect('/')

    else:
        events = []
        apps = StaticHelpers.find_appointments(user_type, user)

        if user_type == StaticHelpers.UserTypes.patient:
            for app in apps:
                events.append({
                    'title': "Appointment with " + str(app.doctor),
                    'description': str(app.notes),
                    'start': str(app.start_time),
                    'end': str(app.end_time)
                })
            form = SelectAppointment(user)
            addForm = AddAppointment(user_type)
            return render(request, 'HealthApp/patientIndex.html', {"events": events, 'form': form, 'addForm': addForm})
        elif user_type == StaticHelpers.UserTypes.doctor or user_type == StaticHelpers.UserTypes.nurse:
            for app in apps:
                events.append({
                    'title': "Appointment with " + str(app.patient),
                    'description': str(app.notes),
                    'start': str(app.start_time),
                    'end': str(app.end_time)
                })
            form = SelectAppointment(user)
            addForm = AddAppointment(user_type)
            return render(request, 'HealthApp/doctorIndex.html', {"events": events, 'form': form, 'addForm': addForm})


def authForm(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        # if user exists and user is active, login
        if user is not None:
            if user.is_active:
                login(request, user)

        return redirect('/')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Login()
        return render(request, 'HealthApp/login.html', {'form': form})


def unauth(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Register(request.POST)
        # check whether it's valid:
        # TODO: Check for valid data
        # if a GET (or any other method) we'll create a blank form
    else:
        form = Register()
    return render(request, 'HealthApp/register.html', {'form': form})
