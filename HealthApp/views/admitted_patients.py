"""
Admitted Patients view

This file contains logic regarding admitted patients and permissions

=== Methods=== 

render_view --- Renders the admitted patients page with permissions based on user type
admitted_patients --- Called when the home view is loaded or a form is submitted

"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from HealthApp import staticHelpers
from HealthApp.forms import SetPatientHospital
from HealthApp.forms.add_prescription import AddPrescription
from HealthApp.forms.admit_patient import AdmitPatient
from HealthApp.forms.discharge_patient import DischargePatient
from HealthApp.forms.send_message import SendMessage
from HealthApp.forms.update_med_info import UpdateMedInfo
from HealthApp.models import Patient


def render_view(request, user_type, user):
    admitted_patients = staticHelpers.get_admitted_patients()
    all_patients = Patient.objects.all()
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

    if user_type == staticHelpers.UserTypes.patient:
        return redirect('/')
    elif user_type == staticHelpers.UserTypes.doctor:
        set_patient_hospital_forms = SetPatientHospital.build_form_dict(all_patients)
        set_patient_admission = staticHelpers.build_set_patient_admission_forms(user_type, all_patients)
        add_prescriptions = AddPrescription.build_form_dict(all_patients)
        prescriptions = staticHelpers.get_prescriptions_dict(all_patients)
        tests = staticHelpers.get_tests_dict(user_type, user, all_patients)
        update_med_info_forms = UpdateMedInfo.build_form_dict(all_patients)

        return render(request, 'HealthApp/admitted_patients.html',
                      {'user_type': user_type, 'admitted_patients': admitted_patients,
                       'set_patient_hospital_forms': set_patient_hospital_forms,
                       'set_patient_admission': set_patient_admission, 'unread_messages': unread_messages,
                       'sendMessage': sendMessage, 'add_prescriptions': add_prescriptions,
                       'update_med_info_forms': update_med_info_forms, 'prescriptions': prescriptions, 'tests': tests})
    elif user_type == staticHelpers.UserTypes.nurse:
        set_patient_admission = staticHelpers.build_set_patient_admission_forms(user_type, all_patients)
        prescriptions = staticHelpers.get_prescriptions_dict(all_patients)
        update_med_info_forms = UpdateMedInfo.build_form_dict(all_patients)

        return render(request, 'HealthApp/admitted_patients.html',
                      {'user_type': user_type, 'admitted_patients': admitted_patients, 'all_patients': all_patients,
                       'set_patient_admission': set_patient_admission, 'prescriptions': prescriptions,
                       'update_med_info_forms': update_med_info_forms, 'unread_messages': unread_messages,
                       'sendMessage': sendMessage})


# Called when the home view is loaded or a form is submitted
@login_required(login_url="login/")
def admitted_patients(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    if user_type == staticHelpers.UserTypes.admin:
        # Redirect an admin over the admin page before trying to pull real user only data
        return redirect('/admin/')
    elif request.method == 'POST':
        if request.POST['form_id'] == 'SendMessage':
            SendMessage.handle_post(user, request.POST)
        elif request.POST['form_id'] == 'AdmitPatient':
            AdmitPatient.handle_post(user_type, user, request.POST)
        elif request.POST['form_id'] == 'DischargePatient':
            DischargePatient.handle_post(user_type, user, request.POST)
        elif request.POST['form_id'] == 'AddPrescription':
            AddPrescription.handle_post(user_type, user, request.POST)
        elif request.POST['form_id'] == 'UpdateMedInfo':
            UpdateMedInfo.handle_post(user_type, user, request.POST)
        elif 'form_id' not in request.POST:
            return redirect('/admitted_patients')

        # Form submit has been handled so redirect as a GET (this way refreshing the page works)
        return redirect('/admitted_patients')
    else:
        return render_view(request, user_type, user)
