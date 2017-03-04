from django.db import models
from .Hospital import Hospital
from .Doctor import Doctor
from .Patient import Patient


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Doctor')
    startTime = models.DateTimeField(default=None, verbose_name='Start Time')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    @classmethod
    def create_appointment(cls, hospital, doctor, patient, startTime, endTime, notes):
        appointment = cls(hospital=hospital, doctor=doctor, patient=patient, startTime=startTime, endTime=endTime,
                          notes=notes)
        appointment.save()
