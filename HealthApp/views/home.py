from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from HealthApp.forms import UpdateAppointment, AddAppointment, UpdatePatient, SetPatientHospital
from HealthApp.models import Hospital, Patient, Doctor, Appointment, LogEntry
from HealthApp import staticHelpers


# Handles submit of the update patient data form
def save_patient(request):
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
    patient.desired_hospital = Hospital.objects.all().filter(id=hospital_id)[0]
    doctor_id = request.POST['doctor']
    patient.primary_doctor = Doctor.objects.all().filter(id=doctor_id)[0]

    patient.save()

    LogEntry.log_action(request.user.username, "Updated their patient data")


# Handles submit of the create and edit appointment forms
def set_appointment(request, user_type, user):
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


# Handles submit of the delete appointment form
def delete_appointment(request):
    Appointment.objects.all().get(id=request.POST['event-id-update']).delete()
    LogEntry.log_action(request.user.username, "Canceled an appointment")


# Renders the home page with the correct data for the current user
def render_view(request, user_type, user):
    events = []
    appointments = staticHelpers.find_appointments(user_type, user)
    patients = staticHelpers.find_patients(user_type, user)

    if user_type == staticHelpers.UserTypes.patient:
        for app in appointments:
            # Don't change the title - it'll break the pre-filling of the update appointment form
            events.append({
                'id': str(app.id),
                'title': "Appointment with " + str(app.doctor),
                'description': str(app.notes),
                'start': str(app.start_time),
                'end': str(app.end_time)
            })
        form = UpdateAppointment(user_type, user)
        add_form = AddAppointment(user_type)
        update_form = UpdatePatient(user)
        return render(request, 'HealthApp/index.html',
                      {"events": events, 'user_type': user_type, 'form': form, 'addForm': add_form,
                       'profileForm': update_form})
    elif user_type == staticHelpers.UserTypes.doctor:
        for app in appointments:
            # Don't change the title - it'll break the pre-filling of the update appointment form
            events.append({
                'id': str(app.id),
                'title': "Appointment with " + str(app.patient),
                'description': str(app.notes),
                'start': str(app.start_time),
                'end': str(app.end_time)
            })

        setPatientHospitalForms = dict()
        for patient in patients:
            setPatientHospitalForms[patient.username] = SetPatientHospital(patient)

        form = UpdateAppointment(user_type, user)
        add_form = AddAppointment(user_type)
        return render(request, 'HealthApp/index.html',
                      {"events": events, 'user_type': user_type, 'form': form, 'addForm': add_form,
                       'patients': patients, 'setPatientHospitalForms': setPatientHospitalForms})
    elif user_type == staticHelpers.UserTypes.nurse:
        for app in appointments:
            # Don't change the title - it'll break the pre-filling of the update appointment form
            events.append({
                'id': str(app.id),
                'title': "Appointment between " + str(app.patient) + " & " + str(app.doctor),
                'description': str(app.notes),
                'start': str(app.start_time),
                'end': str(app.end_time)
            })
        form = UpdateAppointment(user_type, user)
        add_form = AddAppointment(user_type)
        return render(request, 'HealthApp/index.html',
                      {"events": events, 'user_type': user_type, 'form': form, 'addForm': add_form, 'patients': patients})


# Called when the home view is loaded or a form is submitted
@login_required(login_url="login/")
def home(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')
    elif request.method == 'POST':
        # A form was submitted
        if 'first_name' in request.POST:
            save_patient(request)
        elif 'Cancel Appointment' in request.POST:
            delete_appointment(request)
        else:
            set_appointment(request, user_type, user)

        # Form submit has been handled so redirect as a GET (this way refreshing the page works)
        return redirect('/')
    else:
        return render_view(request, user_type, user)
