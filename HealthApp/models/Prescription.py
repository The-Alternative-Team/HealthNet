"""
Prescription model

Django model for prescription.

=== Fields ===

drug -------- (char) Name of the prescribed drug.
doctor ------ (model) The doctor writing the prescription.
patient ----- (model) The patient who the prescription is for.
date -------- (date) The date the prescription was created (automatically is set to current date and uneditable).
refills ----- (integer) Amount of refils (0 for no refills)(make sure it has a max of ~5 in forms).
notes ------- (char) Additional notes for the prescription.

=== Methods ===

__str__ ------------- Returns the string representation of the existing prescription
update_prescription - Updates an existing prescription with the given information

"""

from django.db import models
from .Doctor import Doctor
from .Patient import Patient
from django.utils import timezone
from  HealthApp import staticHelpers


# doctor needs to be automatically set to the doc that is signed in (only docs can write prescriptions)


class Prescription(models.Model):
    drug = models.CharField(max_length=50, verbose_name='Drug Name')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Patient')
    date = models.DateField(auto_now=True, verbose_name='Date prescribed')
    refills = models.IntegerField(verbose_name='Number of Refills')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    def __str__(self):
        return self.drug + " prescription for " + str(self.patient) + " (" + str(self.doctor) + ")"

    def update_prescription(self, drug, doctor, patient, refills, notes):
        self.drug = drug
        self.doctor = doctor
        self.patient = patient
        self.refills = refills
        self.notes = notes
        self.save()
