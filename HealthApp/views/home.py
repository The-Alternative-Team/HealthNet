from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from HealthApp.forms import SelectAppointment, AddAppointment
from HealthApp import StaticHelpers
from HealthApp.models import Patient, Doctor, Appointment


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