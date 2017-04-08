#work in progress model (not in __init__.py)

"""
Prescription model

Django model for prescriptions.

=== Fields ===

drug -------- (char) Name of the prescribed drug.
doctor ------ (model) The doctor writing the prescription.
patient ----- (model) The patient who the prescription is for.
date -------- (date) The date the prescription was created (automatically is set to current date and uneditable).
refills ----- (integer) Amount of refils (0 for no refills)(make sure it has a max of ~5 in forms).
notes ------- (char) Additional notes for the prescription.

=== Methods ===

__str__ ------------- Returns the string representation of the existing prescription

"""
from django.db import models
from .Doctor import Doctor
from .Patient import Patient


class Prescriptions(models.Model):
    drug = models.CharField(max_length=50, verbose_name='Drug Name')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    date = models.DateField(auto_now=True, verbose_name='Date prescribed')
    refills = models.IntegerField(verbose_name='Number of Refills')
    notes = models.CharField(default='', max_length=1000, verbose_name='Notes')

    def __str__(self):
        return self.drug + " Prescription for " + self.patient.__str__()
