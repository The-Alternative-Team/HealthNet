from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from HealthApp.forms import UpdateAppointment, AddAppointment
from HealthApp import staticHelpers
from HealthApp.models import Patient, Doctor, Appointment, LogEntry


@login_required(login_url="login/")
def home(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real-user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')

    if request.method == 'POST':
        # A form was submitted

        # TODO: Figure out which form instead of assuming it was the new appointment form

        if 'Cancel Appointment' not in request.POST:
            # Get appointment_doctor
            if user_type == staticHelpers.UserTypes.nurse:
                doctor_id = int(request.POST['doctor'])
                appointment_doctor = Doctor.objects.all().filter(id=doctor_id)[0]
            elif user_type == staticHelpers.UserTypes.doctor:
                appointment_doctor = user
            else:
                # It's a patient
                appointment_doctor = user.primary_doctor

            # Get appointment_patient
            if user_type == staticHelpers.UserTypes.patient:
                appointment_patient = user
            else:
                patient_id = int(request.POST['patient'])
                appointment_patient = Patient.objects.all().filter(id=patient_id)[0]
            if 'event-id-update' in request.POST:
                Appointment.objects.all().get(id=request.POST['event-id-update']).update_appointment(
                    hospital=appointment_patient.hospital, doctor=appointment_doctor,
                    patient=appointment_patient, start_time=request.POST['start_time'],
                    end_time=request.POST['end_time'], notes=request.POST['notes'])
                LogEntry.log_action(request.user.username, "Updated an appointment")
            else:
                appointment = Appointment(hospital=appointment_patient.hospital, doctor=appointment_doctor,
                                          patient=appointment_patient, start_time=request.POST['start_time'],
                                          end_time=request.POST['end_time'], notes=request.POST['notes'])
                appointment.save()
                LogEntry.log_action(request.user.username, "Created an appointment")
        else:
            Appointment.objects.all().get(id=request.POST['event-id-update']).delete()

        # Redirect as a GET so refreshing works
        return redirect('/')

    else:
        events = []
        apps = staticHelpers.find_appointments(user_type, user)

        if user_type == staticHelpers.UserTypes.patient:
            for app in apps:
                events.append({
                    'id': str(app.id),
                    'title': "Appointment with " + str(app.doctor),
                    'description': str(app.notes),
                    'start': str(app.start_time),
                    'end': str(app.end_time)
                })
            form = UpdateAppointment(user_type)
            addForm = AddAppointment(user_type)
            return render(request, 'HealthApp/patientIndex.html', {"events": events, 'form': form, 'addForm': addForm})
        elif user_type == staticHelpers.UserTypes.doctor or user_type == staticHelpers.UserTypes.nurse:
            for app in apps:
                events.append({
                    'id': str(app.id),
                    'title': "Appointment with " + str(app.patient),
                    'description': str(app.notes),
                    'start': str(app.start_time),
                    'end': str(app.end_time)
                })
            form = UpdateAppointment(user_type)
            addForm = AddAppointment(user_type)
            return render(request, 'HealthApp/doctorIndex.html', {"events": events, 'form': form, 'addForm': addForm})
