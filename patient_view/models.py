from django.db import models

# Create your models here.
class User(models.Model):
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

    email = models.EmailField()
    password = models.CharField()
    first_name = models.CharField(verbose_name="First Name")
    last_name = models.CharField(verbose_name="Last Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    social = models.IntegerField(max_length=9, verbose_name="Social Security Number:")
    address_street = models.CharField(verbose_name="Street")
    address_city = models.CharField(verbose_name="City")
    address_state = models.CharField(choices=STATE_CHOICES, verbose_name="State")
    address_zip = models.IntegerField(max_length=5, verbose_name="Zip Code")
    home_phone = models.BigIntegerField(help_text="No spaces or dashes", max_length=10, verbose_name="Home Phone")
    cell_phone = models.BigIntegerField(help_text="No spaces or dashes", max_length=10, verbose_name="Cell Phone")

class Patient(models.Model, User):
    hospital = models.CharField()
    doctor = models.CharField()
    prescription = []
    test_results = []
    med_info = []
    appointments = []
    desired_hospital = models.CharField(verbose_name="Desired Hospital")
    e_cont_fname = models.CharField(verbose_name="Emergency Contact: First Name")
    e_cont_lname = models.CharField(verbose_name="Emergency Contact: Last Name")
    e_cont_home_phone = models.BigIntegerField(help_text="No spaces or dashes", max_length=10, verbose_name="Emergency Contact: Home Phone")
    e_cont_cell_phone = models.BigIntegerField(help_text="No spaces or dashes", max_length=10, verbose_name="Emergency Contact: Cell Phone")

    def __str__(self):
        return str(self.name)

