from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(User):
    # Inherits from the actual django user object
    # (Get username, email, first name, and last name from this)

    STATE_CHOICES = (
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
        ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
        ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
        ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
        ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))

    date_of_birth = models.DateField(verbose_name="Date of Birth", default=datetime.date.today)
    social = models.IntegerField(verbose_name="Social Security Number:", default=0)
    address_street = models.CharField(max_length=100, verbose_name="Street", default="")
    address_city = models.CharField(max_length=50, verbose_name="City", default="")
    address_state = models.CharField(max_length=50, choices=STATE_CHOICES, verbose_name="State", default="")
    address_zip = models.IntegerField(verbose_name="Zip Code", default=0)
    home_phone = models.BigIntegerField(help_text="No spaces or dashes", verbose_name="Home Phone", default=0)
    cell_phone = models.BigIntegerField(help_text="No spaces or dashes", verbose_name="Cell Phone", default=0)

    def __str__(self):
        return self.user.username + "'s UserProfile"