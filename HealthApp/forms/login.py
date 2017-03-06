from django.contrib.auth.forms import AuthenticationForm


class Login(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(Login, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-Mail'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password'}
