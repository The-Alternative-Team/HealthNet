# work in progress model (not in __init__.py)


"""
Medical Info model

Django model for Medical Info.

=== Fields ===

patient -------------- (model) The patient who the prescription is for.
time ----------------- (datetime) The date and time these stats were recorded (automatically set to now)
heart rate ----------- (integer) Patient's heart rate in beats per minute
Systolic pressure ---- (integer) Patient's Systolic blood pressure in mmHg
Diastolic pressure --- (integer) Patient's Diastolic blood pressure in mmHg 
Body Temp ------------ (integer) Patient's body temperature in degree Fahrenheit 
Respiratory rate ----- (integer) Patient's respiratory rate in breaths per minute
notes ---------------- (char) Additional notes for Medical Info.

=== Methods ===

__str__ ------------- Returns the string representation of the existing MedInfo

"""
from django.db import models
from .Patient import Patient


class MedInfo(models.Model):
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    time = models.DateTimeField(auto_now=True, verbose_name='Time recorded')
    heart_rate = models.IntegerField(help_text='beats per minute', verbose_name='Heart Rate')
    systolic_pressure = models.IntegerField(help_text='mmHg', verbose_name='Systolic Blood Pressure')
    diastolic_pressure = models.IntegerField(help_text='mmHg', verbose_name='Diastolic Blood Pressure')
    body_temp = models.IntegerField(help_text='Fahrenheit', verbose_name='Body Temperature')
    respiratory_rate = models.IntegerField(help_text='breaths per minute', verbose_name='Respiratory Rate')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    def __str__(self):
        return self.patient.__str__() + "'s Medical Info"

    def update_medInfo(self, patient, time, heart_rate, systolic_pressure, diastolic_pressure, body_temp,
                       respiratory_rate, notes):
        self.patient = patient
        self.time = time
        self.heart_rate = heart_rate
        self.systolic_pressure = systolic_pressure
        self.diastolic_pressure = diastolic_pressure
        self.body_temp = body_temp
        self.respiratory_rate = respiratory_rate
        self.notes = notes
        self.save()
