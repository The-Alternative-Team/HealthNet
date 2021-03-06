"""
Appointment model

Django model for an appointment between a Patient and a Doctor.

=== Fields ===

hospital ---- (model) The hospital in which the appointment will take place.
doctor ------ (model) The doctor assigned to the appointment.
patient ----- (model) The patient who the appointment is for.
start_time -- (datetime) The time the appointment will start at.
end_time ---- (datetime) The time the appointment should end at.
notes ------- (char) Additional notes for the appointment.

=== Methods ===

__str__ ------------- Returns the string representation of the existing appointment
update_appointment -- Static method that updates fields for an appointment

"""

from django.db import models

from .Doctor import Doctor
from .Hospital import Hospital
from .Patient import Patient


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    def __str__(self):
        return "appointment at " + str(self.start_time) + "."

    def update_appointment(self, hospital, doctor, patient, start_time, end_time, notes):
        self.hospital = hospital
        self.doctor = doctor
        self.patient = patient
        self.start_time = start_time
        self.end_time = end_time
        self.notes = notes
        self.save()
