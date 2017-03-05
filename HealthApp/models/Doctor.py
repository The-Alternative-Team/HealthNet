from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital


class Doctor(UserProfile):
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Hospital')
    #appointments = []
    #patients = []

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return str(self.name)
