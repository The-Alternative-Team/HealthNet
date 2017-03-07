from django.shortcuts import render, redirect
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from HealthApp.forms import Register
from HealthApp.models import Hospital, Doctor, Patient, LogEntry


def register(request):
    errors = []
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            # TODO: Cry about mismatched passwords
            return redirect("/register")
        try:
            password_validation.validate_password(password1)
        except ValidationError:
            # TODO: Cry about bad passwords
            return redirect("/register")

        email = request.POST['username']  # TODO: Figure out what happens with duped usernames
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        social = request.POST['social']
        address_street = request.POST['address_street']
        address_city = request.POST['address_city']
        address_state = request.POST['address_state']
        address_zip = request.POST['address_zip']
        home_phone = request.POST['home_phone']
        cell_phone = request.POST['cell_phone']
        e_cont_fname = request.POST['e_cont_fname']
        e_cont_lname = request.POST['e_cont_lname']
        e_cont_home_phone = request.POST['e_cont_home_phone']
        e_cont_cell_phone = request.POST['e_cont_cell_phone']
        # TODO: Validate this data (and steal their identity)

        hospital_id = request.POST['hospital']
        hospital = Hospital.objects.all().filter(id=hospital_id)[0]
        doctor_id = request.POST['doctor']
        doctor = Doctor.objects.all().filter(id=doctor_id)[0]

        # Create patient
        patient = Patient(username=email, first_name=first_name, last_name=last_name,
                          date_of_birth=date_of_birth, social=social, address_street=address_street,
                          address_city=address_city, address_state=address_state, address_zip=address_zip,
                          home_phone=home_phone, cell_phone=cell_phone, desired_hospital=hospital, hospital=hospital,
                          primary_doctor=doctor, e_cont_fname=e_cont_fname, e_cont_lname=e_cont_lname,
                          e_cont_home_phone=e_cont_home_phone, e_cont_cell_phone=e_cont_cell_phone)
        patient.set_password(password1)

        # catches invalid data and refreshes page with no error message(right now)
        try:
            patient.save()
        except (IntegrityError, ValidationError):
            return redirect("/register")

        # Log them in
        user = authenticate(username=email, password=password1)
        login(request, user)

        LogEntry.log_action(request.user.username, "Registered and logged in")

        return redirect("/")
    else:
        form = Register()
        return render(request, 'HealthApp/register.html', {'form': form})
