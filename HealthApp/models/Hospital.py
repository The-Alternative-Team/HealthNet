from django.db import models

from HealthApp.statesList import STATE_CHOICES


class Hospital(models.Model):
    name = models.CharField(max_length=50, default='', verbose_name='Hospital Name')
    street = models.CharField(max_length=100, default='', verbose_name='Street Address')
    city = models.CharField(max_length=50, default='', verbose_name='Town/City')
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default=None, verbose_name='State')
    zipCode = models.IntegerField(help_text="Please enter the 5 digit zip code", default=None,
                                  verbose_name='Zip Code')
    phoneNumber = models.BigIntegerField(help_text="No spaces or dashes", default=None,
                                         verbose_name='Phone Number')

    def __str__(self):
        return self.name
