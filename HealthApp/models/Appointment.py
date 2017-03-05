from django.db import models
from .Hospital import Hospital
from .Doctor import Doctor
from .Patient import Patient
import datetime


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    @classmethod
    def create_appointment(cls, hospital, doctor, patient, start_time, end_time, notes):
        appointment = cls(hospital=hospital, doctor=doctor, patient=patient, start_time=start_time, end_time=end_time,
                          notes=notes)
        appointment.save()

    def update_appointment(self, hospital, doctor, patient, start_time, end_time, notes):
        self.hospital = hospital
        self.doctor = doctor
        self.patient = patient
        self.start_time = start_time
        self.end_time = end_time
        self.notes = notes
        self.save()
