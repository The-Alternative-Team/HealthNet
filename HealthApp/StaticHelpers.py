from HealthApp.models.Doctor import Doctor
from HealthApp.models.Patient import Patient
from HealthApp.models.Nurse import Nurse

# A set of static utility functions


# Takes a base user object and returns a list that contains the user's type as a String and the most complete
#   instance of the user's database object
def user_to_subclass(user):
    # It's a Patient
    try:
        return ["Patient", Patient.objects.get(username=user.username)]
    except Patient.DoesNotExist:
        pass

    # It's a Doctor
    try:
        return ["Doctor", Doctor.objects.get(username=user.username)]
    except Doctor.DoesNotExist:
        pass

    # It's a Nurse
    try:
        return ["Nurse", Nurse.objects.get(username=user.username)]
    except Nurse.DoesNotExist:
        pass

    # It's an Admin
    return ["Admin", user]