from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital


class Nurse(UserProfile):
    hospital = models.ForeignKey(Hospital, verbose_name='Hospital')
    #patients = []

    class Meta:
        verbose_name = "Nurse"
        verbose_name_plural = "Nurses"

    def __str__(self):
        return "Nurse " + self.username
