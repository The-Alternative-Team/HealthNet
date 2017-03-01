from django.db import models


class Patient(models.Model):
    hospital = models.CharField(max_length=50)
    doctor = models.CharField(max_length=50)
    prescription = []
    test_results = []
    med_info = []
    appointments = []
    desired_hospital = models.CharField(max_length=50, verbose_name="Desired Hospital")
    e_cont_fname = models.CharField(max_length=50, verbose_name="Emergency Contact: First Name")
    e_cont_lname = models.CharField(max_length=50, verbose_name="Emergency Contact: Last Name")
    e_cont_home_phone = models.BigIntegerField(help_text="No spaces or dashes",
                                               verbose_name="Emergency Contact: Home Phone")
    e_cont_cell_phone = models.BigIntegerField(help_text="No spaces or dashes",
                                               verbose_name="Emergency Contact: Cell Phone")

    def __str__(self):
        return str(self.name)
