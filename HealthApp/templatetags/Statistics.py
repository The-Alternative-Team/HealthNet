"""
Statistics 

Provides functions that return system statistics that can be viewed by the system administrator.

=== Methods ===

round --------------------- Given a float and a number of digits to round by, the function rounds the float 
                            to the given number of digits.
                            
                :parameter (float) num ----- number to be rounded
                           (int) precision - number of digits to round by
                :return (float) the float 'num' after it has been rounded

number_admitted_patients -- Queries the database for all admitted patients in the system and returns them in
                            a list.
                            
                :parameter
                :return (List[database objects]) list of patients objects currently admitted into a hospital

avg_visits ---------------- Queries the database for all the patients and admission logs, and returns the 
                            average amount of admissions per patient.
                            
                :parameter
                :return (float) Average admissions per patient.

avg_length_of_stay -------- Queries the database for all the patients and admission logs, and returns the 
                            average length of admission per patient.
                
                :parameter
                :return (float) Average length of admission per patient.

avg_prescriptions --------- Queries the database for all the patients and prescriptions, and returns the
                            average amount of prescriptions per patient.
                                            
                :parameter
                :return (float) Average amount of prescriptions per patient.

num_logs ------------------ Queries the database for all the log entries, and returns the amount of logged
                            actions in the system.
              
                :parameter
                :return (int) Number of logged actions in the system.

"""

from django import template
import datetime
import math

from HealthApp.staticHelpers import *
from HealthApp.models import AdmissionLog, Patient, Prescription, LogEntry

register = template.Library()


# Rounds a float to the given number of digits after the decimal
def round(num, precision):
    return math.ceil(num * (10 ** precision)) / (10 ** precision)


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

    return round(avg, 2)


# in days
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
        avg = total_length_of_stay.total_seconds() / num_admissions
    except ZeroDivisionError:
        avg = 0

    return round(avg * (1.1574 * 10 ** -5), 3)


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

    return round(avg, 2)


@register.simple_tag
def num_logs():
    return len(LogEntry.objects.all())
