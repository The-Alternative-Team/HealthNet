from django.db import models
from .Doctor import Doctor
from .Patient import Patient
from .UploadedFile import UploadedFile


class Test(models.Model):
    date = models.DateTimeField(verbose_name='Test Date')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    file = models.ForeignKey(UploadedFile, verbose_name='Test File')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    def __str__(self):
        return self.patient.__str__() + "'s Test Results for " + self.date.strftime(
            '%B %d, %Y') + " at " + self.date.strftime(
            '%I:%M %p') + "."

    def update_test(self, date, doctor, patient, file, notes):
        self.date = date
        self. doctor = doctor
        self.patient = patient
        self.file = file
        self.notes = notes

    