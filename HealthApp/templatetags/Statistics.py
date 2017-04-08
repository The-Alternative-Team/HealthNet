from django import template
import datetime

from HealthApp.staticHelpers import *
from HealthApp.models import AdmissionLog, Patient, Prescription

register = template.Library()


@register.simple_tag
def number_admitted_patients():
    return len(get_admitted_patients())


@register.simple_tag
def avg_visits():
    try:
        admissions_list = AdmissionLog.objects.all()
    except AdmissionLog.DoesNotExist:
        admissions_list = []
    try:
        patient_list = Patient.objects.all()
    except Patient.DoesNotExist:
        patient_list = []
    admissions_number = len(admissions_list)
    patient_number = len(patient_list)
    try:
        avg = admissions_number / patient_number
    except ZeroDivisionError:
        avg = 0
    return avg


@register.simple_tag
def avg_length_of_stay():
    total_length_of_stay = datetime.timedelta(0)
    try:
        log_list = AdmissionLog.objects.all().filter(admitStatus=False)
        for log in log_list:
            total_length_of_stay += (log.timeDischarged - log.timeAdmitted)
    except AdmissionLog.DoesNotExist:
        log_list = []
    num_admissions = len(log_list)
    try:
        avg = total_length_of_stay / num_admissions
    except ZeroDivisionError:
        avg = 0
    return avg


@register.simple_tag
def avg_prescriptions():
    try:
        prescription_list = Prescription.objects.all()
    except Patient.DoesNotExist:
        prescription_list = []
    try:
        patient_list = Patient.objects.all()
    except Patient.DoesNotExist:
        patient_list = []
    prescription_number = len(prescription_list)
    patient_number = len(patient_list)
    try:
        avg = prescription_number / patient_number
    except ZeroDivisionError:
        avg = 0
    return avg