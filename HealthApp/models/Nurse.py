from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital


class Nurse(UserProfile):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')

    # The patients list is a many to one relationship so it's defined on the 'many' side only
    # See: https://docs.djangoproject.com/en/1.9/topics/db/examples/many_to_one/

    class Meta:
        verbose_name = "Nurse"
        verbose_name_plural = "Nurses"

    def __str__(self):
        return "Nurse " + self.first_name + " " + self.last_name + " (" + self.username + ")"
