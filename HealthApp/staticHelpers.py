from HealthApp.models.Doctor import Doctor
from HealthApp.models.Patient import Patient
from HealthApp.models.Nurse import Nurse
from HealthApp.models import Appointment

# A set of static utility functions

# Static definitions of the user type strings used by user_to_subclass() below
class UserTypes:
    patient = "Patient"
    doctor = "Doctor"
    nurse = "Nurse"
    admin = "Admin"

# Takes a base user object and returns a list that contains the user's type as a string and the most complete
#   instance of the user's database object
def user_to_subclass(user):
    # It's a Patient
    try:
        return UserTypes.patient, Patient.objects.get(username=user.username)
    except Patient.DoesNotExist:
        pass

    # It's a Doctor
    try:
        return UserTypes.doctor, Doctor.objects.get(username=user.username)
    except Doctor.DoesNotExist:
        pass

    # It's a Nurse
    try:
        return UserTypes.nurse, Nurse.objects.get(username=user.username)
    except Nurse.DoesNotExist:
        pass

    # It's an Admin
    return UserTypes.admin, user


# Gets the list of appointments for the given user with the given type
def find_appointments(user_type, user):
    user_id = user.userprofile_ptr_id
    if user_type == UserTypes.nurse:
        # Nurses can view all appointments
        return Appointment.objects.all()
    elif user_type == UserTypes.doctor:
        # Doctors get their appointments only
        return Appointment.objects.all().filter(doctor_id=user_id)
    elif user_type == UserTypes.patient:
        # Patients get their appointments only
        return Appointment.objects.all().filter(patient_id=user_id)