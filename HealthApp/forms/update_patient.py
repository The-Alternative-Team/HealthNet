from django import forms

from HealthApp import statesList
from HealthApp.models import Doctor
from HealthApp.models import Hospital
from HealthApp import staticHelpers


class UpdatePatient(forms.BaseForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='First Name', max_length=100)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Last Name', max_length=100)
    address_street = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
        label='Street', max_length=100)
    address_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        label='City', max_length=100)
    address_state = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'State'}),
        choices=statesList.STATE_CHOICES, label='State')
    address_zip = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
        label='Zip Code')
    home_phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Home Phone Number')
    cell_phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Cell Phone Number')
    e_cont_fname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='Emergency Contact: First Name', max_length=100)
    e_cont_lname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Emergency Contact: Last Name', max_length=100)
    e_cont_home_phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Emergency Contact: Home Phone Number')
    e_cont_cell_phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123)456-7890'}),
        label='Emergency Contact: Cell Phone Number')

    # Query for hospitals on form generate
    def __init__(self, user):
        super().__init__()

        user_type, patient = staticHelpers.user_to_subclass(user)
        print(patient)

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
