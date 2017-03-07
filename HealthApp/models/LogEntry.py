"""
LogEntry model

Django model for a log entry.

=== Fields ===

userMail -- (model) The email of the user that generated the event.
time ------ (dateTime) The time that the logged event took place.
action ---- (char) The event that took place.

=== Methods ===

log_action -- Static method that creates a LogEntry object and saves it in the SQLite database.
__str__ ----- Returns the string representation of the existing LogEntry.

"""

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
