from django.db import models
from .User import User
from .Hospital import Hospital


class Nurse(User):
    hospital = models.ForeignKey(Hospital, default=None, verbose_name='Hospital')
    patients = []

    def __str__(self):
        return str(self.name)
