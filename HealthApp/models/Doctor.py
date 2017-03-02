from django.db import models
from .User import User
from .Hospital import Hospital


class Doctor(User):
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Hospital')
    appointments = []
    patients = []

    def __str__(self):
        return str(self.name)
