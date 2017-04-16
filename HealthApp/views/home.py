from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register

from HealthApp.forms import UpdateAppointment, AddAppointment, UpdatePatient, SetPatientHospital
from HealthApp.forms.admit_patient import AdmitPatient
from HealthApp.forms.send_message import SendMessage
from HealthApp.models import Hospital, Patient, Doctor, Appointment, LogEntry, Message
from HealthApp import staticHelpers
from django.utils import timezone


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


# Handles submit of the add and update appointment forms
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
    all_patients = Patient.objects.all()
    admitted_patients = staticHelpers.get_admitted_patients()
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

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
                       'profileForm': update_form, 'unread_messages': unread_messages, 'sendMessage': sendMessage})
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

        set_patient_hospital_forms = dict()
        for patient in all_patients:
            set_patient_hospital_forms[patient.username] = SetPatientHospital(patient)

        set_patient_admission = dict()
        for patient in all_patients:
            set_patient_admission[patient.username] = AdmitPatient(patient)

        form = UpdateAppointment(user_type, user)
        add_form = AddAppointment(user_type)
        return render(request, 'HealthApp/index.html',
                      {"events": events, 'user_type': user_type, 'form': form, 'addForm': add_form,
                       'patients': patients, 'all_patients': all_patients, 'admitted_patients': admitted_patients,
                       'set_patient_hospital_forms': set_patient_hospital_forms,
                       'set_patient_admission': set_patient_admission,
                       'unread_messages': unread_messages, 'sendMessage': sendMessage})
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
                      {"events": events, 'user_type': user_type, 'form': form, 'addForm': add_form,
                       'patients': patients, 'admitted_patients': admitted_patients, 'unread_messages': unread_messages,
                       'sendMessage': sendMessage})


# Handles submit of the transfer patient data form
def set_patient_hospital(request):
    user_type, doctor = staticHelpers.user_to_subclass(request.user)

    if user_type == staticHelpers.UserTypes.doctor:
        patient_id = request.POST['patient_id']
        patient = Patient.objects.all().filter(id=patient_id)[0]

        hospital_id = request.POST['hospital']
        patient.hospital = Hospital.objects.all().filter(id=hospital_id)[0]

        patient.save()

        LogEntry.log_action(request.user.username, "Transferred patient " + patient.username + " to " +
                            patient.hospital.name)


@register.filter(name='get_item')
def get_item(dictionary, key):
    print(dictionary)
    return dictionary.get(key)  # Called when the home view is loaded or a form is submitted


@login_required(login_url="login/")
def home(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')
    elif request.method == 'POST':
        # A form was submitted so handle based on id
        if request.POST['form_id'] == 'UpdatePatient':
            save_patient(request)
        elif request.POST['form_id'] == 'UpdateAppointment' or request.POST['form_id'] == 'AddAppointment':
            if 'Cancel Appointment' in request.POST:
                delete_appointment(request)
            else:
                set_appointment(request, user_type, user)
        elif request.POST['form_id'] == 'SetPatientHospital':
            set_patient_hospital(request)
        elif request.POST['form_id'] == 'SendMessage':
            time = timezone.now()
            message = Message(subject=request.POST['subject'], body=request.POST['body'], sender=user.username,
                              recipient=request.POST['recipient'], sent_at=time)
            message.save()

        # Form submit has been handled so redirect as a GET (this way refreshing the page works)
        return redirect('/')
    else:
        return render_view(request, user_type, user)
