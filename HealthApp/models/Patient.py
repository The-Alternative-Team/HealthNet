"""
Patient model

Django model for a Patient. Inherits UserProfile

=== Fields ===

hospital ----------- (model) The hospital in which the Nurse actively works.
primary_doctor ----- (model) The patient's primary doctor.
desired_hospital --- (model) The patient's hospital of choice.
e_cont_fname ------- (char) The first name of the patient's emergency contact.
e_cont_lname ------- (char) The last name of the patient's emergency contact.
e_cont_home_phone -- (integer) The home phone number of the patient's emergency contact.
e_cont_cell_phone -- (integer) The cell phone number of the patiend's emergency contact.

=== Methods ===

__str__ --------- Returns the string representation of the existing Patient object.
update_patient -- Updates the fields of an existing Patient object.

"""

from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital
from .Doctor import Doctor


class Patient(UserProfile):
    hospital = models.ForeignKey(Hospital, related_name="current_hospital", verbose_name='Hospital')
    primary_doctor = models.ForeignKey(Doctor, related_name='Doctor', verbose_name='Doctor')
    desired_hospital = models.ForeignKey(Hospital, related_name="desired_hospital", verbose_name='Desired Hospital')
    e_cont_fname = models.CharField(max_length=50, verbose_name="Emergency Contact: First Name")
    e_cont_lname = models.CharField(max_length=50, verbose_name="Emergency Contact: Last Name")
    e_cont_home_phone = models.BigIntegerField(help_text="No spaces or dashes",
                                               verbose_name="Emergency Contact: Home Phone")
    e_cont_cell_phone = models.BigIntegerField(help_text="No spaces or dashes",
                                               verbose_name="Emergency Contact: Cell Phone")

    # The appointments list is a many to one relationship so it's defined on the 'many' side only
    # See: https://docs.djangoproject.com/en/1.9/topics/db/examples/many_to_one/

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return "Patient " + self.first_name + " " + self.last_name + " (" + self.username + ")"
