from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital


class Nurse(UserProfile):
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Hospital')
    #patients = []

    def __str__(self):
        return str(self.name)
