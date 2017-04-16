"""
staticHelpers

Provides easy access to functions that perform cross-model db calls and other support work.

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
    
    
find_message -- Takes a user parameter and returns an ordered list of all messages sent to them. 

    :parameter (database object) user - The user to obtain messages for.
    :returns (list of database objects) - A list of messages sent to the user in question ordered by date sent.
    
                
find_unread_messages --  Takes a user parameter and returns an ordered list of all unread messages sent to them. 

    :parameter (database object) user - The user to obtain messages for.
    :returns (list of database objects) - A list of unread messages sent to the user in question ordered by date sent.
    
    
find_patients -- Returns a list of patients that the given doctor or nurse are responsible for.

    :parameter (database object) user - The user to obtain relevant patients for.
               (string) user_type - The user type determined by user_to_subclass 
    :returns (list of database objects) - A list of patients applicable to the given doctor/nurse. 
    

get_admitted_patients -- Returns a list of admitted patients (should be for specified hospital)
    :parameter  
    :returns
    
    
set_form_id -- Sets an id for a form so it can be easily detected on POST

"""

from django import forms

from HealthApp.models.Doctor import Doctor
from HealthApp.models.Patient import Patient
from HealthApp.models.Nurse import Nurse
from HealthApp.models.Appointment import Appointment
from HealthApp.models.Message import Message
from HealthApp.models.AdmissionLog import AdmissionLog


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


def find_messages(user):
    username = user.username
    return Message.objects.all().filter(recipient=username).order_by("-sent_at")


def find_unread_messages(user):
    username = user.username
    return Message.objects.all().filter(recipient=username, unread=True).order_by("-sent_at")


# Builds the list of patients the given doctor or nurse is responsible for
def find_patients(user_type, user):
    user_id = user.userprofile_ptr_id
    if user_type == UserTypes.doctor:
        # Doctors get their patients
        return Patient.objects.all().filter(primary_doctor_id=user_id)
    if user_type == UserTypes.nurse:
        # Nurses get all patients at their hospital
        return Patient.objects.all().filter(hospital=user.hospital)


# TODO: add hospital parameter
def get_admitted_patients():
    patient_list = []
    try:
        log_list = AdmissionLog.objects.all().filter(admitStatus=True)
        for log in log_list:
            patient = Patient.objects.filter(username=log.userMail)
            patient_list.extend(patient)
    except AdmissionLog.DoesNotExist:
        pass
    return patient_list


# Sets an id for a form so it can be easily detected on POST
def set_form_id(form, id):
    form.fields['form_id'] = forms.CharField(widget=forms.HiddenInput(), initial=id)
