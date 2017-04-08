from .staticHelpers import *
from HealthApp.models.AdmissionLog import AdmissionLog
from HealthApp.models.Patient import Patient
from HealthApp.models.Prescription import Prescriptions
from datetime import datetime

'''
NOT TESTED
'''
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
    total_length_of_stay = datetime.timedelta(0)
    log_list = AdmissionLog.objects.all().filter(admitStatus=False)
    num_admissions = len(log_list)
    for log in log_list:
        total_length_of_stay += (log.timeDischarged - log.timeAdmitted)
    avg = total_length_of_stay / num_admissions
    return avg

def avg_prescriptions():
    prescription_list = Prescriptions.objects.all()
    patient_list = Patient.objects.all()
    prescription_number = len(prescription_list)
    patient_number = len(patient_list)
    avg = prescription_number / patient_number
    return avg
