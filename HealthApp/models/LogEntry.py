from django.db import models


class LogEntry(models.Model):
    userMail = models.CharField(default='', max_length=100, verbose_name='User Email')
    time = models.DateTimeField(default=None, verbose_name='Date Logged')
    action = models.CharField(default='', max_length=1000, verbose_name='Action')

    def __str__(self):
        return self.userMail + " did " + self.action
