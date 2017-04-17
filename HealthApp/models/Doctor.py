"""
Doctor model

Django model for a Doctor. Inherits UserProfile

=== Fields ===

hospital -- (model) The hospital in which the Doctor actively works.

=== Methods ===

__str__ -- Returns the string representation of the existing Doctor object.

"""

from django.db import models

from .Hospital import Hospital
from .UserProfile import UserProfile


class Doctor(UserProfile):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')

    # The appointments and patients lists are many to one relationships so they're defined on the 'many' side only
    # See: https://docs.djangoproject.com/en/1.9/topics/db/examples/many_to_one/

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    # Don't change this - it'll break the pre-filling of the update appointment form
    def __str__(self):
        return "Dr. " + self.first_name + " " + self.last_name + " (" + self.username + ")"
