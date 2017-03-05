from django.db import models
from .UserProfile import UserProfile
from .Hospital import Hospital
from .Doctor import Doctor


class Patient(UserProfile):
    hospital = models.ForeignKey(Hospital, related_name="current_hospital", default=None, verbose_name='Hospital')
    Doctor = models.ForeignKey(Doctor, related_name='Doctor', default=None, verbose_name='Doctor')
    #prescription = []
    #test_results = []
    #med_info = []
    #appointments = []
    desired_hospital = models.ForeignKey(Hospital, related_name="desired_hospital", default=None,
                                         verbose_name='Desired Hospital')
    e_cont_fname = models.CharField(max_length=50, verbose_name="Emergency Contact: First Name")
    e_cont_lname = models.CharField(max_length=50, verbose_name="Emergency Contact: Last Name")
    e_cont_home_phone = models.BigIntegerField(help_text="No spaces or dashes",
                                               verbose_name="Emergency Contact: Home Phone")
    e_cont_cell_phone = models.BigIntegerField(help_text="No spaces or dashes",
                                               verbose_name="Emergency Contact: Cell Phone")

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return "Patient " + self.username


    # Not needed anymore for now
    # @classmethod
    # def create_patient(cls, first_name, last_name, email, password, hospital, doctor, desired_hospital, e_cont_fname,
    #                    e_cont_lname, e_cont_home_phone, e_cont_cell_phone):
    #     # Create the user object first
    #     user = User.objects.create_user(email, password=password)
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
    #
    #     # Now create and save the patient
    #     patient = cls(user=user, hospital=hospital, Doctor=doctor, desired_hospital=desired_hospital, e_cont_fname=e_cont_fname, e_cont_lname=e_cont_lname, e_cont_home_phone=e_cont_home_phone, e_cont_cell_phone=e_cont_cell_phone)
    #     patient.save()