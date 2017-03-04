from django import forms
from .models import Hospital, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Register(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                 label='First Name', max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                label='Last Name', max_length=100)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '01/01/1950'}),
        label='Date of Birth')
    social = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-45-6789'}),
                             label='Social Security Number', max_length=12)
    address_street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
                                     label='Street', max_length=100)
    address_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                                   label='City', max_length=100)
    address_state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'State'}),
                                      choices=UserProfile.STATE_CHOICES, label='State')
    address_zip = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
                                     label='Zip Code')
    home_phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Home Phone Number')
    cell_phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Cell Phone Number')

    # Query for hospitals on form generate
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)

        # Generate hospital ChoiceField
        hospitalTuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))

        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}), choices=hospitalTuple,
            label='Hospital')

        # Style django's user registration fields
        self.fields['username'].widget.attrs = {'class': 'form-control'}
        self.fields['password1'].widget.attrs = {'class': 'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(Register, self).save(commit=False)
        user.email = self.cleaned_data['username']
        user.first_name = self.cleaned_data['First name']
        user.last_name = self.cleaned_data['Last name']

        if commit:
            user.save()

        return user