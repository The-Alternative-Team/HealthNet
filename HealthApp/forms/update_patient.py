from django import forms

from HealthApp import statesList, staticHelpers
from HealthApp.models import Doctor, LogEntry, Patient


class UpdatePatient(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        staticHelpers.set_form_id(self, "UpdatePatient")

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

        self.fields['doctor'] = forms.ChoiceField(initial={'doctor': patient.primary_doctor},
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control', 'placeholder': 'Doctor'}),
                                                  choices=doctor_tuple,
                                                  label='Doctor')

    class Meta:
        model = Patient
        fields = ('first_name', 'last_name')

    @classmethod
    def handle_post(cls, user_type, patient, post_data):
        if user_type == staticHelpers.UserTypes.patient:
            patient.first_name = post_data['first_name']
            patient.last_name = post_data['last_name']
            patient.address_street = post_data['address_street']
            patient.address_city = post_data['address_city']
            patient.address_state = post_data['address_state']
            patient.address_zip = post_data['address_zip']
            patient.home_phone = post_data['home_phone']
            patient.cell_phone = post_data['cell_phone']
            patient.e_cont_fname = post_data['e_cont_fname']
            patient.e_cont_lname = post_data['e_cont_lname']
            patient.e_cont_home_phone = post_data['e_cont_home_phone']
            patient.e_cont_cell_phone = post_data['e_cont_cell_phone']

            # TODO: Validate this data (and steal their identity) before saving it

            doctor_id = post_data['doctor']
            patient.primary_doctor = Doctor.objects.get(id=doctor_id)

            patient.save()

            LogEntry.log_action(patient.username, "Updated their patient data")