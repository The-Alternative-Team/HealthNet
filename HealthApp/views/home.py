from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from HealthApp import staticHelpers
from HealthApp.forms import UpdateAppointment, AddAppointment, UpdatePatient, SetPatientHospital
from HealthApp.forms.add_prescription import AddPrescription
from HealthApp.forms.admit_patient import AdmitPatient
from HealthApp.forms.discharge_patient import DischargePatient
from HealthApp.forms.send_message import SendMessage
from HealthApp.forms.update_med_info import UpdateMedInfo
from HealthApp.models import Patient


# Renders the home page with the correct data for the current user
#   dictOverrides: Fill this with name-form pairs to over ride (such as a validated form)
def render_view(request, user_type, user, dictOverrides=dict()):
    events = []
    appointments = staticHelpers.find_appointments(user_type, user)
    patients = staticHelpers.find_patients(user_type, user)
    all_patients = Patient.objects.all()

    for app in appointments:
        # Don"t change the title - it"ll break the pre-filling of the update appointment form
        title = ""
        if user_type == staticHelpers.UserTypes.patient:
            title = "Appointment with " + str(app.doctor)
        elif user_type == staticHelpers.UserTypes.doctor:
            title = "Appointment with " + str(app.patient)
        elif user_type == staticHelpers.UserTypes.nurse:
            title = "Appointment between " + str(app.patient) + " & " + str(app.doctor)

        events.append({
            "id": str(app.id),
            "title": title,
            "description": str(app.notes),
            "start": str(app.start_time),
            "end": str(app.end_time)
        })

    add_app_form = AddAppointment(user_type, user)
    update_app_form = UpdateAppointment(user_type, user)
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)
    dataDict = {"events": events, "user_type": user_type, "add_app_form": add_app_form, 
                "update_app_form": update_app_form, "unread_messages": unread_messages, "sendMessage": sendMessage}

    if user_type == staticHelpers.UserTypes.patient:
        update_form = UpdatePatient(patient=user)
        prescriptions = staticHelpers.get_patient_prescriptions(user)
        tests = staticHelpers.get_patient_tests(user_type, user, user)

        dataDict.update({"profileForm": update_form, "prescriptions": prescriptions, "tests": tests})
    elif user_type == staticHelpers.UserTypes.doctor:
        set_patient_hospital_forms = SetPatientHospital.build_form_dict(all_patients)
        update_med_info_forms = UpdateMedInfo.build_form_dict(all_patients)
        add_prescriptions = AddPrescription.build_form_dict(all_patients)
        prescriptions = staticHelpers.get_prescriptions_dict(all_patients)
        tests = staticHelpers.get_tests_dict(user_type, user, all_patients)
        set_patient_admission = staticHelpers.build_set_patient_admission_forms(user_type, all_patients)
        admitted_patients = staticHelpers.get_admitted_patients(user.hospital)

        dataDict.update({"patients": patients, "all_patients": all_patients, "admitted_patients": admitted_patients,
                         "set_patient_hospital_forms": set_patient_hospital_forms,
                         "update_med_info_forms": update_med_info_forms, "set_patient_admission": set_patient_admission,
                         "add_prescriptions": add_prescriptions, "prescriptions": prescriptions, "tests": tests})
    elif user_type == staticHelpers.UserTypes.nurse:
        set_patient_admission = staticHelpers.build_set_patient_admission_forms(user_type, all_patients)
        update_med_info_forms = UpdateMedInfo.build_form_dict(all_patients)
        prescriptions = staticHelpers.get_prescriptions_dict(all_patients)
        admitted_patients = staticHelpers.get_admitted_patients(user.hospital)

        dataDict.update({"patients": patients, "all_patients": all_patients, "admitted_patients": admitted_patients,
                         "set_patient_admission": set_patient_admission, "update_med_info_forms": update_med_info_forms,
                         "prescriptions": prescriptions})

    dataDict.update(dictOverrides)
    return render(request, "HealthApp/index.html", dataDict)

@login_required(login_url="login/")
def home(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    if user_type == staticHelpers.UserTypes.admin:
        # Redirect an admin over the admin page before trying to pull real user only data
        return redirect("/admin/")
    elif request.method == "POST":
        # A form was submitted so handle based on id
        failedFormDict = dict()
        if request.POST["form_id"] == "UpdatePatient":
            UpdatePatient.handle_post(user_type, user, request.POST, failedFormDict)
        elif request.POST["form_id"] == "UpdateAppointment" or request.POST["form_id"] == "AddAppointment":
            UpdateAppointment.handle_post(user_type, user, request.POST, failedFormDict)
        elif request.POST["form_id"] == "SetPatientHospital":
            SetPatientHospital.handle_post(user_type, user, request.POST)
        elif request.POST["form_id"] == "SendMessage":
            SendMessage.handle_post(user, request.POST)
        elif request.POST["form_id"] == "AdmitPatient":
            AdmitPatient.handle_post(user_type, user, request.POST)
        elif request.POST["form_id"] == "DischargePatient":
            DischargePatient.handle_post(user_type, user, request.POST)
        elif request.POST["form_id"] == "AddPrescription":
            AddPrescription.handle_post(user_type, user, request.POST)
        elif request.POST["form_id"] == "UpdateMedInfo":
            UpdateMedInfo.handle_post(user_type, user, request.POST)

        return render_view(request, user_type, user, dictOverrides=failedFormDict)

    else:
        return render_view(request, user_type, user)
