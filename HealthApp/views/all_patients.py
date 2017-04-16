from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.template.defaulttags import register

from HealthApp import staticHelpers
from HealthApp.forms import SetPatientHospital
from HealthApp.forms.add_prescription import AddPrescription
from HealthApp.forms.admit_patient import AdmitPatient
from HealthApp.forms.discharge_patient import DischargePatient
from HealthApp.forms.send_message import SendMessage
from HealthApp.forms.update_med_info import UpdateMedInfo
from HealthApp.models import Patient, Message, AdmissionLog, Hospital, Prescription, LogEntry


def render_view(request, user_type, user):
    patients = staticHelpers.find_patients(user_type, user)
    all_patients = Patient.objects.all()
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

    if user_type == staticHelpers.UserTypes.patient:
        return redirect('/')
    elif user_type == staticHelpers.UserTypes.doctor:
        set_patient_hospital_forms = dict()
        for patient in all_patients:
            set_patient_hospital_forms[patient.username] = SetPatientHospital(patient)
        set_patient_admission = dict()
        for patient in all_patients:
            if staticHelpers.get_admitted_patients().__contains__(patient):
                set_patient_admission[patient.username] = DischargePatient(patient)
            else:
                set_patient_admission[patient.username] = AdmitPatient(patient)

        add_prescriptions = dict()
        prescriptions = dict()
        for patient in all_patients:
            add_prescriptions[patient.username] = AddPrescription(patient)
            prescriptions[patient.username] = staticHelpers.get_all_prescriptions(patient)

        update_med_info_forms = dict()
        for patient in all_patients:
            update_med_info_forms[patient.username] = UpdateMedInfo(patient)

        return render(request, 'HealthApp/all_patients.html',
                      {'user_type': user_type, 'patients': patients, 'unread_messages': unread_messages,
                       'set_patient_admission': set_patient_admission, 'all_patients': all_patients,
                       'add_prescriptions': add_prescriptions, 'prescriptions': prescriptions, 'update_med_info_forms': update_med_info_forms,
                       'set_patient_hospital_forms': set_patient_hospital_forms, 'sendMessage': sendMessage})
    elif user_type == staticHelpers.UserTypes.nurse:
        set_patient_admission = dict()
        for patient in all_patients:
            if not staticHelpers.get_admitted_patients().__contains__(patient):
                set_patient_admission[patient.username] = AdmitPatient(patient)

        prescriptions = dict()
        for patient in all_patients:
            prescriptions[patient.username] = staticHelpers.get_all_prescriptions(patient)

        update_med_info_forms = dict()
        for patient in all_patients:
            update_med_info_forms[patient.username] = UpdateMedInfo(patient)

        return render(request, 'HealthApp/all_patients.html',
                      {'user_type': user_type, 'patients': patients, 'unread_messages': unread_messages,
                       'set_patient_admission': set_patient_admission, 'all_patients': all_patients,
                       'prescriptions': prescriptions, 'sendMessage': sendMessage, 'update_med_info_forms': update_med_info_forms})

    @register.filter(name='get_item')
    def get_item(dictionary, key):
        return dictionary.get(key)  # Called when the home view is loaded or a form is submitted


# Called when the home view is loaded or a form is submitted
@login_required(login_url="login/")
def all_patients(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    if user_type == staticHelpers.UserTypes.admin:
        # Redirect an admin over the admin page before trying to pull real user only data
        return redirect('/admin/')
    elif request.method == 'POST':
        if request.POST['form_id'] == 'SendMessage':
            Message.handlePost(user.username, request.POST)
        elif request.POST['form_id'] == 'AdmitPatient':
            admit_patient = AdmissionLog(userMail=request.POST['userMail'], reason=request.POST['reason'],
                                         timeAdmitted=timezone.now(), admittedBy=user.username,
                                         hospital=Hospital.objects.all().filter(id=request.POST['hospital'])[0],
                                         admitStatus=True)
            admit_patient.save()
            LogEntry.log_action(user.username, ("admitted " + request.POST['userMail']))
        elif request.POST['form_id'] == 'DischargePatient':
            user_mail = request.POST['userMail']
            log_entry = AdmissionLog.objects.all().filter(userMail=user_mail, admitStatus=True)[0]
            log_entry.admitStatus = False
            log_entry.dischargedBy = user.username
            log_entry.timeDischarged = timezone.now()
            log_entry.save()
            LogEntry.log_action(user.username, ("discharged " + user_mail))
        elif request.POST['form_id'] == 'AddPrescription':
            prescription = Prescription(drug=request.POST['drug'], doctor=user,
                                        patient=Patient.objects.all().filter(username=request.POST['patient'])[0],
                                        date=timezone.now(), refills=request.POST['refills'],
                                        notes=request.POST['notes'])
            prescription.save()
        elif 'form_id' not in request.POST:
            return redirect('/all_patients')

            # Form submit has been handled so redirect as a GET (this way refreshing the page works)
        return redirect('/all_patients')
    else:
        return render_view(request, user_type, user)
