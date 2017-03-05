from django.db import models
from django.contrib.auth.models import User
from .StatesList import STATE_CHOICES


class UserProfile(User):
    # Inherits from the actual django user object
    # (Get username, email, first name, and last name from this)

    date_of_birth = models.DateField(verbose_name="Date of Birth")
    social = models.IntegerField(verbose_name="Social Security Number:")
    address_street = models.CharField(max_length=100, verbose_name="Street")
    address_city = models.CharField(max_length=50, verbose_name="City")
    address_state = models.CharField(max_length=50, choices=STATE_CHOICES, verbose_name="State")
    address_zip = models.IntegerField(verbose_name="Zip Code")
    home_phone = models.BigIntegerField(help_text="No spaces or dashes", verbose_name="Home Phone")
    cell_phone = models.BigIntegerField(help_text="No spaces or dashes", verbose_name="Cell Phone")

    User._meta.get_field('username').verbose_name = 'Username (aka email)'
    User._meta.get_field('email').verbose_name = 'Email (don\'t need this)'

    def __str__(self):
        return self.username + "'s UserProfile"