from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from HealthApp.forms import UpdateAppointment, AddAppointment
from HealthApp import staticHelpers
from HealthApp.forms import UpdatePatient
from HealthApp.models import Hospital
from HealthApp.models import Patient, Doctor, Appointment, LogEntry


@login_required(login_url="login/")
def home(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real-user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')

    if request.method == 'POST':
        # A form was submitted
        if 'first_name' in request.POST:
            user_type, patient = staticHelpers.user_to_subclass(request.user)

            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.address_street = request.POST['address_street']
            patient.address_city = request.POST['address_city']
            patient.address_state = request.POST['address_state']
            patient.address_zip = request.POST['address_zip']
            patient.home_phone = request.POST['home_phone']
            patient.cell_phone = request.POST['cell_phone']
            patient.e_cont_fname = request.POST['e_cont_fname']
            patient.e_cont_lname = request.POST['e_cont_lname']
            patient.e_cont_home_phone = request.POST['e_cont_home_phone']
            patient.e_cont_cell_phone = request.POST['e_cont_cell_phone']
            # TODO: Validate this data (and steal their identity) before saving it

            hospital_id = request.POST['hospital']
            patient.hospital = Hospital.objects.all().filter(id=hospital_id)[0]
            patient.desired_hospital = patient.hospital
            doctor_id = request.POST['doctor']
            patient.primary_doctor = Doctor.objects.all().filter(id=doctor_id)[0]

            patient.save()

            LogEntry.log_action(request.user.username, "Updated data")

        elif 'Cancel Appointment' not in request.POST:
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
            updateForm = UpdatePatient(user)
            return render(request, 'HealthApp/patientIndex.html',
                          {"events": events, 'form': form, 'addForm': addForm, 'profileForm': updateForm})
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
