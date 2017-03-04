from django.db import models
from django.utils import timezone


class LogEntry(models.Model):
    userMail = models.CharField(default='', max_length=100, verbose_name='User Email')
    time = models.DateTimeField(default=None, verbose_name='Date Logged')
    action = models.CharField(default='', max_length=1000, verbose_name='Action Completed')

    @classmethod
    def log_action(cls, userMail, action):
        log = cls(userMail=userMail, action=action, time=timezone.now())
        log.save()

    def __str__(self):
        return self.userMail + " did " + self.action + " at " + str(self.time)