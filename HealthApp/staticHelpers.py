"""
staticHelpers

Module that includes methods that are often utilized.

=== Methods ===

user_to_subclass --- Takes a base Django user object as input and returns a tuple that contains the user
                     type as a string and the most complete database object of the UserProfile.

    :parameter (database object) user - The user to obtain data about.
    :returns (tuple) The user type as a string and the most complete database object of the UserProfile


find_appointments -- Takes two the parameters that are returned by user_to_subclass and returns a list
                     of database objects representing appointments relevant to the user.

    :parameter (database object) user - The user to obtain relevant appointments for.
               (string) user_type - The user type determined by user_to_subclass
    :returns (list of database objects) - A list of appointments relevant to the user in question.

"""

from HealthApp.models.Doctor import Doctor
from HealthApp.models.Patient import Patient
from HealthApp.models.Nurse import Nurse
from HealthApp.models import Appointment


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
        # Nurses can view all appointments in their hospital
        return Appointment.objects.all().filter(hospital=user.hospital)
    elif user_type == UserTypes.doctor:
        # Doctors get their appointments only
        return Appointment.objects.all().filter(doctor_id=user_id)
    elif user_type == UserTypes.patient:
        # Patients get their appointments only
        return Appointment.objects.all().filter(patient_id=user_id)


# Builds the list of patients the given doctor or nurse is responsible for
def find_patients(user_type, user):
    user_id = user.userprofile_ptr_id
    if user_type == UserTypes.doctor:
        # Doctors get their patients
        return Patient.objects.all().filter(primary_doctor_id=user_id)
    if user_type == UserTypes.nurse:
        # Doctors get their patients
        return Patient.objects.all().filter(hospital=user.hospital)
