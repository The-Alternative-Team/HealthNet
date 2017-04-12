"""
Admission Log model

Django model for an admission log for a Patient.

=== Fields ===

userMail ----- (char) The email ID of the patient admitted to the hospital.
reason ------- (char) The reason for the patient's visit.
timeAdmitted - (datetime) The time the patient is admitted. 
admittedBy --- (char) The email ID of the person who admitted the patient to the hospital.
hospital ----- (model) The hospital in which the patient is admitted.
timeDischarged (datetime) The time the patient is discharged.
dischargedBy - (char) The email ID of the person who discharged the patient from the hospital.
admitStatus -- (boolean) The status of whether the patient is currently admitted in a hospital.

=== Methods ===

__str__ ------------- Returns the string representation of the admission log.
admit_patient ------- Class method that creates an admission log object and saves it in the SQLite database.
discharge_patient --- Static method that discharges a patient in an existing admission log and saves it.
"""

from django.db import models
from django.utils import timezone
from .Hospital import Hospital


class AdmissionLog(models.Model):
    userMail = models.CharField(default='', max_length=100, verbose_name='User Email')
    reason = models.CharField(default='', max_length=250, verbose_name='reason')
    timeAdmitted = models.DateTimeField(default=None, verbose_name='Time Admitted')
    admittedBy = models.CharField(default='', max_length=100, verbose_name='Admitted by')
    hospital = models.ForeignKey(Hospital, default=None, related_name="Hospital", verbose_name="Hospital")
    timeDischarged = models.DateTimeField(default=None, verbose_name='Time Discharged')
    dischargedBy = models.CharField(default='', max_length=100, verbose_name='Discharged by')
    admitStatus = models.BooleanField(default=False, verbose_name="Admission Status")
    class Meta:
        verbose_name = "Admission Log entry"
        verbose_name_plural = "Admission Log entries"

    @classmethod
    def admit_patient(cls, user_mail, admitted_by, hospital):
        log = cls(userMail=user_mail, timeAdmitted=timezone.now(), admittedBy=admitted_by, hospital=hospital,
                  admitStatus=True)
        log.save()

    def discharge_patient(self, discharged_by):
        self.timeDischarged = timezone.now()
        self.dischargedBy = discharged_by
        self.admitStatus = False
        self.save()

    def __str__(self):
        return self.userMail + " was admitted at " + self.timeAdmitted.strftime(
            '%B %d, %Y  %I:%M %p') + " by " + self.admittedBy
