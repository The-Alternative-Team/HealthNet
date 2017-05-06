"""
Send Message form

Django form for sending a message.

=== Fields ===

recipient -- (ChoiceField) user that the message will be sent to
subject ---- (CharField) the subject of the message
body ------- (CharField) the body of the message

=== Methods ===

__init__ --------- Initializes the form.
handle_post ------ Creates a message given a completed form.

"""

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from HealthApp.models import Message, LogEntry
from HealthApp.staticHelpers import set_form_id, user_to_subclass, UserTypes


class SendMessage(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()
        set_form_id(self, "SendMessage")

        user_tuple = []
        for user in User.objects.all().order_by("first_name"):
            theirUserType, user = user_to_subclass(user)
            
            if not (user_type == UserTypes.patient and theirUserType == UserTypes.patient):
                user_tuple.append((user.username, str(user)))

        self.fields['recipient'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'User'}), choices=user_tuple,
            label='recipient')

        # CharFields
        self.fields['subject'].widget.attrs = {'class': 'form-control', 'placeholder': 'Subject'}

        # TextField
        self.fields['body'].widget.attrs = {'class': 'form-control', 'placeholder': 'Message'}

    class Meta:
        model = Message
        fields = ['subject', 'body', 'recipient']

    @classmethod
    def handle_post(cls, user, post_data):
        message = Message(subject=post_data['subject'], body=post_data['body'], sender=user.username,
                          recipient=post_data['recipient'], sent_at=timezone.now())
        message.save()
        LogEntry.log_action(user.username, "Sent a message to " + post_data['recipient'])