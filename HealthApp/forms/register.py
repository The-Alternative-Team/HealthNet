"""
Register form

Django form for patient registration

=== Fields ===

first_name --------- (CharField) first name of the patient.
last_name ---------- (CharField) last name of the patient.
username ----------- (EmailField) email of the patient.
password1 ---------- (PasswordField) password of the patient
password2 ---------- (PasswordField) confirmation of 'password1'
date_of_birth ------ (DateField) date of birth of the patient.
social ------------- (CharField) social security number of the patient.
address_street ----- (CharField) address street of the patient.
address_City ------- (CharField) address city of the patient
address_state ------ (ChoiceField) address state of the patient
address_zip -------- (IntegerField) zip code of the patient
home_phone --------- (IntegerField) home phone number of the patient
cell_phone --------- (IntegerField) cell phone number of the patient
e_cont_fname ------- (CharField) first name of patient's emergency contact
e_cont_lname ------- (CharField) last name of patient's emergency contact
e_cont_home_phone -- (IntegerField) home phone of patient's emergency contact
e_cont_cell_phone -- (IntegerField) cell phone of patient's emergency contact
doctor ------------- (ChoiceField) list of doctors available for choice by the patient.
hospital ----------- (ChoiceField) list of hospitals available for choice by the patient

=== Methods ===

__init__ ----- Initializes the form.
is_valid -- validates the completed form and throws system errors if invalid.

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from HealthApp import statesList
from HealthApp import validate
from HealthApp.models import Doctor
from HealthApp.models import Hospital


class Register(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='First Name', max_length=100)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Last Name', max_length=100)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        label='Date of Birth')
    social = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-45-6789'}),
        label='Social Security Number', max_length=12)
    address_street = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
        label='Street', max_length=100)
    address_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        label='City', max_length=100)
    address_state = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'State'}),
        choices=statesList.STATE_CHOICES, label='State')
    address_zip = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
        label='Zip Code')
    home_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Home Phone Number')
    cell_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Cell Phone Number')
    e_cont_fname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='Emergency Contact: First Name', max_length=100)
    e_cont_lname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Emergency Contact: Last Name', max_length=100)
    e_cont_home_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Emergency Contact: Home Phone Number')
    e_cont_cell_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Emergency Contact: Cell Phone Number')

    # Query for hospitals on form generate
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)

        # Generate hospital ChoiceField
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))
        # Generate doctor ChoiceField
        doctor_tuple = tuple(Doctor.objects.all().values_list("id", "first_name").order_by("first_name"))

        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=hospital_tuple,
            label='Hospital')

        self.fields['doctor'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Doctor'}), choices=doctor_tuple,
            label='Doctor')

        # Style django's user registration fields
        self.fields['username'] = forms.EmailField(widget=forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'E-Mail'}))
        self.fields['username'].help_text = None
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password'}
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm Password'}
        self.fields['password2'].help_text = None

    # custom validation allows for custom error messages
    def is_valid(self):
        # run the parent validation first
        valid = super(Register, self).is_valid()

        # if it doesn't pass standard validation it will break custom validation. So return here
        if not valid:
            return valid

        try:
            validate.phone(self.cleaned_data['home_phone'])
        except forms.ValidationError as e:
            self.add_error('home_phone', e.code)
            valid = False
        try:
            validate.phone(self.cleaned_data['cell_phone'])
        except forms.ValidationError as e:
            self.add_error('cell_phone', e.code)
            valid = False
        try:
            validate.phone(self.cleaned_data['e_cont_home_phone'])
        except forms.ValidationError as e:
            self.add_error('e_cont_home_phone', e.code)
            valid = False
        try:
            validate.phone(self.cleaned_data['e_cont_cell_phone'])
        except forms.ValidationError as e:
            self.add_error('e_cont_cell_phone', e.code)
            valid = False
        try:
            validate.ssn(self.cleaned_data['social'])
        except forms.ValidationError as e:
            self.add_error('social', e.code)
            valid = False
        try:
            validate.zip(self.cleaned_data['address_zip'])
        except forms.ValidationError as e:
            self.add_error('address_zip', e.code)
            valid = False

        return valid

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
