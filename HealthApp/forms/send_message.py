from django import forms
from django.contrib.auth.models import User

from HealthApp.models import Message
from HealthApp.staticHelpers import set_form_id


class SendMessage(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()
        set_form_id(self, "SendMessage")

        user_tuple = tuple(User.objects.all().values_list("username", "username").order_by("username"))

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
