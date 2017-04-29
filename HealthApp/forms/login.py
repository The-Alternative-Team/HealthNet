"""
Login form

Django form for logging in.

=== Fields ===

username -- (CharField) email ID of the user logging in
password -- (CharField) password of the user logging in
=== Methods ===

__init__ -- Initializes the form.
"""

from django.contrib.auth.forms import AuthenticationForm


class Login(AuthenticationForm):
    def __init__(self, isRetry, request=None, *args, **kwargs):
        self.request = request
        super(Login, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-Mail'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password'}

        self.isRetry = isRetry

