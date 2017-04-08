from django.db import models
from django.utils import timezone
from .Hospital import Hospital


class AdmissionLog(models.Model):
    userMail = models.CharField(default='', max_length=100, verbose_name='User Email')
    reason = models.CharField(default='', max_length=250, verbose_name='reason')
    timeAdmitted = models.DateTimeField(default=None, verbose_name='Time Admitted')
    admittedBy = models.CharField(default='', max_length=100, verbose_name='Admitted by')
    hospital = models.ForeignKey(Hospital, related_name="Hospital", verbose_name="Hospital")
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

    def __str__(self):
        return self.userMail + " was admitted at " + self.timeAdmitted.strftime(
            '%B %d, %Y  %I:%M %p') + " by " + self.admittedBy
