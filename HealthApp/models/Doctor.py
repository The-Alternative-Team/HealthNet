from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital


class Doctor(UserProfile):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')

    # The appointments and patients lists are many to one relationships so they're defined on the 'many' side only
    # See: https://docs.djangoproject.com/en/1.9/topics/db/examples/many_to_one/

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return "Doctor " + self.username
