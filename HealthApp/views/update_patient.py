from django.shortcuts import render, redirect
from HealthApp.forms import UpdatePatient
from HealthApp.models import Hospital, Doctor, Patient, LogEntry
from HealthApp import staticHelpers


def update_patient(request):
    if request.method == 'POST':
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

        return redirect("/")
    else:
        form = UpdatePatient(request.user)
        return render(request, 'HealthApp/register.html', {'form': form})
