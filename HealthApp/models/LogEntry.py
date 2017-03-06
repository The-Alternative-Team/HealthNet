from django.db import models
from django.utils import timezone


class LogEntry(models.Model):
    userMail = models.CharField(default='', max_length=100, verbose_name='User Email')
    time = models.DateTimeField(default=None, verbose_name='Date Logged')
    action = models.CharField(default='', max_length=1000, verbose_name='Action Completed')

    class Meta:
        verbose_name = "Log Entry"
        verbose_name_plural = "Log Entries"
    @classmethod
    def log_action(cls, user_mail, action):
        log = cls(userMail=user_mail, action=action, time=timezone.now())
        log.save()

    def __str__(self):
        return self.userMail + " " + self.action + " at " + self.time.strftime('%B %d, %Y  %I:%M %p')