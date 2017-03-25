from django import forms

from HealthApp import statesList
from HealthApp.models import Doctor, Hospital, Patient


class UpdatePatient(forms.ModelForm):
    # Query for hospitals on form generate
    def __init__(self, patient):
        super().__init__()

        # TODO: Use patient obj to fill in form

        # Generate hospital ChoiceField
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))
        # Generate doctor ChoiceField
        doctor_tuple = tuple(Doctor.objects.all().values_list("id", "first_name").order_by("first_name"))

        self.fields['first_name'] = forms.CharField(initial=patient.first_name,
                                                    widget=forms.TextInput(
                                                        attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                                    label='First Name', max_length=100)
        self.fields['last_name'] = forms.CharField(initial=patient.last_name,
                                                   widget=forms.TextInput(
                                                       attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                                   label='Last Name', max_length=100)
        self.fields['address_street'] = forms.CharField(initial=patient.address_street,
                                                        widget=forms.TextInput(
                                                            attrs={'class': 'form-control', 'placeholder': 'Street'}),
                                                        label='Street', max_length=100)
        self.fields['address_city'] = forms.CharField(initial=patient.address_city,
                                                      widget=forms.TextInput(
                                                          attrs={'class': 'form-control', 'placeholder': 'City'}),
                                                      label='City', max_length=100)
        self.fields['address_state'] = forms.ChoiceField(initial=patient.address_state,
                                                         widget=forms.Select(
                                                             attrs={'class': 'form-control', 'placeholder': 'State'}),
                                                         choices=statesList.STATE_CHOICES, label='State')
        self.fields['address_zip'] = forms.IntegerField(initial=patient.address_zip,
                                                        widget=forms.TextInput(
                                                            attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
                                                        label='Zip Code')
        self.fields['home_phone'] = forms.IntegerField(initial=patient.home_phone,
                                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                     'placeholder': '(123)456-7890'}),
                                                       label='Home Phone Number')
        self.fields['cell_phone'] = forms.IntegerField(initial=patient.cell_phone,
                                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                     'placeholder': '(123)456-7890'}),
                                                       label='Cell Phone Number')
        self.fields['e_cont_fname'] = forms.CharField(initial=patient.e_cont_fname,
                                                      widget=forms.TextInput(
                                                          attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                                      label='Emergency Contact: First Name', max_length=100)
        self.fields['e_cont_lname'] = forms.CharField(initial=patient.e_cont_lname,
                                                      widget=forms.TextInput(
                                                          attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                                      label='Emergency Contact: Last Name', max_length=100)
        self.fields['e_cont_home_phone'] = forms.IntegerField(initial=patient.e_cont_home_phone,
                                                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'placeholder': '(123)456-7890'}),
                                                              label='Emergency Contact: Home Phone Number')
        self.fields['e_cont_cell_phone'] = forms.IntegerField(initial=patient.e_cont_cell_phone,
                                                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'placeholder': '(123)456-7890'}),
                                                              label='Emergency Contact: Cell Phone Number')

        self.fields['hospital'] = forms.ChoiceField(initial={'hospital': patient.hospital},
                                                    widget=forms.Select(
                                                        attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
                                                    choices=hospital_tuple,
                                                    label='Hospital')

        self.fields['doctor'] = forms.ChoiceField(initial={'doctor': patient.primary_doctor},
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control', 'placeholder': 'Doctor'}),
                                                  choices=doctor_tuple,
                                                  label='Doctor')

    class Meta:
        model = Patient
        fields = ('first_name', 'last_name')
