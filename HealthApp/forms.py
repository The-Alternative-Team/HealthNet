from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from HealthApp import StatesList, StaticHelpers
from .models import Hospital, Doctor, Appointment


class Login(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(Login, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-Mail'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password'}


class Register(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='First Name', max_length=100)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Last Name', max_length=100)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY'}),
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
        choices=StatesList.STATE_CHOICES, label='State')
    address_zip = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
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
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))
        # Generate hospital ChoiceField
        doctor_tuple = tuple(Doctor.objects.all().values_list("id", "user_ptr").order_by("user_ptr"))

        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=hospital_tuple,
            label='Hospital')

        self.fields['doctor'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Doctor'}), choices=doctor_tuple,
            label='Doctor')

        # Style django's user registration fields
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-Mail'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm Password'}

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


class SelectAppointment(forms.Form):
    def __init__(self, user):
        super().__init__()
        appointment_tuple = tuple(
            Appointment.objects.all().values_list("id", "start_time").order_by("start_time").filter(
                patient_id=user.userprofile_ptr_id))
        self.fields['appointments'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=appointment_tuple,
            label='Appointments')


class AddAppointment(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()

        # Only allow nurses to set custom doctors
        if user_type == StaticHelpers.UserTypes.nurse:
            self.fields['doctor'].widget.attrs = {'class': 'form-control', 'placeholder': 'Doctor'}
        else:
            del self.fields['doctor']

        # Don't allow patients to set a custom patient
        if user_type != StaticHelpers.UserTypes.patient:
            self.fields['patient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Patient'}
        else:
            del self.fields['doctor']

        self.fields['start_time'].widget.attrs = {'class': 'form-control', 'placeholder': 'Start Time: (MM/DD/YYYY HH:MM:SS)'}
        self.fields['end_time'].widget.attrs = {'class': 'form-control', 'placeholder': 'End Time: (MM/DD/YYYY HH:MM:SS)'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'start_time', 'end_time', 'notes']
