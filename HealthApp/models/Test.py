"""
Test model

Django model for a test.

=== Fields ===

date -------- (dateTime) The time that the test was administered.
doctor ------ (model) The doctor administering the test.
patient ----- (model) The patient being tested.
notes ------- (char) Additional notes for the test.
releaseStatus (boolean) A boolean value that is default False. This value determines if a patient has permission to
                        view the test.
=== Methods ===

__str__ ------------- Returns the string representation of the existing test.
release_test -------- Sets the releaseStatus boolean value to True.
get_attached_files -- Queries the list of files that are associated with this test.
"""

from datetime import datetime

from django.db import models

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

    def release_test(self):
        self.releaseStatus = True

    def get_attached_files(self):
        from .TestFile import TestFile
        try:
            return TestFile.objects.filter(test=self.id)
        except TestFile.DoesNotExist:
            return []
