from django import forms

from HealthApp.models import Message


class SendMessage(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()

        # DateTimes
        self.fields['sent_at'].widget.attrs = {'class': 'form-control', 'placeholder': 'Sent at: (YYYY-MM-DD HH:MM)'}
        self.fields['read_at'].widget.attrs = {'class': 'form-control', 'placeholder': 'Read at: (YYYY-MM-DD HH:MM)'}

        # CharFields
        self.fields['sender'].widget.attrs = {'class': 'form-control', 'placeholder': 'Sender'}
        self.fields['subject'].widget.attrs = {'class': 'form-control', 'placeholder': 'Sender'}
        self.fields['recipient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Recipient'}

        # BoolField
        self.fields['unread'].widget.attrs = {}  # this is a bool, not sure what to put

        # TestField
        self.fields['body'].widget.attrs = {'class': 'form-control', 'placeholder': 'Sender'}
        # is a textfield hadled differently than a charfield?

    class Meta:
        model = Message
        fields = ['subject', 'body', 'sender', 'recipient', 'sent_at', 'read_at', 'unread']
