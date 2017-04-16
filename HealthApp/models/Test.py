"""
Test model

Django model for a test.

=== Fields ===

date -------- (dateTime) The time that the test was administered.
doctor ------ (model) The doctor administering the test.
patient ----- (model) The patient being tested.
file -------- (model) The file containing the test results/information.
notes ------- (char) Additional notes for the test.
releaseStatus (boolean) A boolean value that is default False. This value determines if a patient has permission to
                        view the test.
=== Methods ===

__str__ ------------- Returns the string representation of the existing test.
update_test --------- Updates the fields of the test.
release_test -------- Sets the releaseStatus boolean value to True.

"""

from django.db import models
from datetime import datetime

from .Doctor import Doctor
from .Patient import Patient


class Test(models.Model):
    date = models.DateTimeField(default=datetime.now, verbose_name='Test Date')
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name='Patient', blank=True, null=True)
    notes = models.TextField(blank=True, verbose_name='Notes')
    releaseStatus = models.BooleanField(default=False, verbose_name='Released to Patient Status')

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        if self.patient is None:
            return "Empty test result created by " + str(self.doctor)
        else:
            return str(self.patient) + "'s test results for " + self.date.strftime('%B %d, %Y') + " at " + \
                   self.date.strftime('%I:%M %p') + "."

    def update_test(self, date, doctor, patient, file, notes):
        self.date = date
        self.doctor = doctor
        self.patient = patient
        self.file = file
        self.notes = notes
        self.save()

    def release_test(self):
        self.releaseStatus = True

    def get_attached_files(self):
        from .TestFile import TestFile
        return TestFile.objects.all(test=self.id)
