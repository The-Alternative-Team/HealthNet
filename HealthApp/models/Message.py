"""
Message model

Django model for a message set from one registered user to another.

=== Fields ===

subject ---- (char) The subject of the message.
body ------- (text) The body of the message.
sender ----- (char) The email address of the registered user who sent the message.
recipient -- (char) The email address of the registered user of whom the message was sent to.
sent_at ---- (datetime) The time in which the sender sent the message.
read_at ---- (datetime) The time in which the recipient opened the message.
unread ----- (boolean) A boolean which is True if the message has not been read.

=== Methods ===

__str__ -------- Returns the string representation of the message object. If the message was read,
                 string will contain additional info on when it was read.
is_unread ------ Returns boolean value for unread
mark_read ------ Static method that sets the read_at datetime field to the current time. 
                 Sets unread boolean field to False. Event is logged.
get_sender ----- Returns the email address of the registered user who sent the message.
get_recipient -- Returns the email address of the registered user of whom the message was sent to.

"""
from django.db import models
from django.utils import timezone

from HealthApp.models import LogEntry


class Message(models.Model):
    SUBJECT_MAX_LENGTH = 120

    subject = models.CharField(default='', max_length=SUBJECT_MAX_LENGTH, verbose_name='subject')
    body = models.TextField(blank=True, verbose_name='body')

    sender = models.CharField(default='', max_length=100, verbose_name='sender email')
    recipient = models.CharField(default='', max_length=100, verbose_name='recipient email')

    sent_at = models.DateTimeField(verbose_name='sent at')
    read_at = models.DateTimeField(verbose_name='read at', blank=True, null=True)
    unread = models.BooleanField(verbose_name='unread', default=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def is_unread(self):
        return self.unread

    def get_sender(self):
        return self.sender

    def get_recipient(self):
        return self.recipient

    def mark_read(self):
        self.unread = False
        self.read_at = timezone.now()
        self.save()
        LogEntry.log_action(self.recipient, "Read message from " + self.sender)

    def __str__(self):
        string = "Message sent on " + self.sent_at.strftime('%B %d, %Y') + " at " + self.sent_at.strftime(
            '%I:%M:%p') + " from " + self.sender + " to " + self.recipient + " ."
        if not self.unread:
            string += " The message was read on " + self.read_at.strftime('%B %d, %Y') + " at " + self.read_at.strftime(
                '%I:%M:%p') + " ."
        return string

    @classmethod
    def sendNotifMessage(cls, recipient, subject, body):
        message = Message(subject=subject, body=body, sender="HealthNet System",
                          recipient=recipient, sent_at=timezone.now())
        message.save()
