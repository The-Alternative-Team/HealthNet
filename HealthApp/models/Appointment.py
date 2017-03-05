from django.db import models
from .Hospital import Hospital
from .Doctor import Doctor
from .Patient import Patient


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    start_time = models.DateTimeField(verbose_name='Start Time')
    duration = models.IntegerField(help_text="Enter time in minutes", verbose_name='Duration')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    @classmethod
    def create_appointment(cls, hospital, doctor, patient, start_time, end_time, notes):
        appointment = cls(hospital=hospital, doctor=doctor, patient=patient, startTime=start_time, endTime=end_time,
                          notes=notes)
        appointment.save()