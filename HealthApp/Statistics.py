from .staticHelpers import *
from HealthApp.models.AdmissionLog import AdmissionLog
from HealthApp.models.Patient import Patient



def number_admitted_patients():
    return len(get_admitted_patients())


def avg_visits():
    admissions_list = AdmissionLog.objects.all()
    patient_list = Patient.objects.all()
    admissions_number = len(admissions_list)
    patient_number = len(patient_list)
    avg = admissions_number / patient_number
    return avg


def avg_length_of_stay():
    pass
