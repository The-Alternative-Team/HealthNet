from HealthApp.models.Doctor import Doctor
from HealthApp.models.Patient import Patient
from HealthApp.models.Nurse import Nurse
from HealthApp.models import Appointment

# A set of static utility functions

# Static definitions of the user type strings used by user_to_subclass() below
class userTypes:
    patient = "Patient"
    doctor = "Doctor"
    nurse = "Nurse"
    admin = "Admin"

# Takes a base user object and returns a list that contains the user's type as a string and the most complete
#   instance of the user's database object
def user_to_subclass(user):
    # It's a Patient
    try:
        return userTypes.patient, Patient.objects.get(username=user.username)
    except Patient.DoesNotExist:
        pass

    # It's a Doctor
    try:
        return userTypes.doctor, Doctor.objects.get(username=user.username)
    except Doctor.DoesNotExist:
        pass

    # It's a Nurse
    try:
        return userTypes.nurse, Nurse.objects.get(username=user.username)
    except Nurse.DoesNotExist:
        pass

    # It's an Admin
    return userTypes.admin, user


def find_appointments(user):
    user_id = user.userprofile_ptr_id
    return Appointment.objects.all().filter(patient_id=user_id)
