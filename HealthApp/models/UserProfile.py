"""
UserProfile model

Django superclass model for a user profile.

=== Fields ===

date_of_birth --- (date) The user's DOB.
social ---------- (integer) The user's social security number.
address_street -- (char) The street the user lives on.
address_city ---- (char) The city the user lives in.
address_state --- (char) The state the user lives in.
address_zip ----- (integer) The zip code of the user's residence.
home_phone ------ (integer) The user's home phone number.
cell_phone ------ (integer) The user's cell phone number.

=== Methods ===

__str__ -- Returns the string representation of the existing UserProfile object.

"""

from django.contrib.auth.models import User
from django.db import models
from HealthApp.statesList import STATE_CHOICES


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
