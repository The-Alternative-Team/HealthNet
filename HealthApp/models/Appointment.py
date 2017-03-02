from django.db import models
from .Hospital import Hospital
from .Doctor import Doctor
from .Patient import Patient


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Doctor')
    startTime = models.DateTimeField(default=None, verbose_name='Start Time')
    endTime = models.DateTimeField(default=None, verbose_name='End Time')
