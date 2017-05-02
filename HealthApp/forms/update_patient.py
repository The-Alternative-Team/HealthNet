"""
Update Patient Information form

Django form for updating patient information.

=== Fields ===

first_name --------- (CharField) first name of the patient.
last_name ---------- (CharField) last name of the patient.
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
doctor ------------- (ChoiceField) list of doctors avaliable for choice for the patient.

=== Methods ===

__init__ ----- Initializes the form.
handle_post -- Updates patient info given a completed form.

"""

from django import forms

from HealthApp import statesList, staticHelpers, validate
from HealthApp.models import Doctor, LogEntry, Patient


class UpdatePatient(forms.ModelForm):
    def __init__(self, patient=None, postData=None):
        super().__init__(postData, instance=patient)

        staticHelpers.set_form_id(self, "UpdatePatient")

        # Generate doctor ChoiceField
        doctor_tuple = tuple(Doctor.objects.all().values_list("id", "first_name").order_by("first_name"))

        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'First Name'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Last Name'}
        self.fields['address_street'].widget.attrs = {'class': 'form-control', 'placeholder': 'Street'}
        self.fields['address_city'].widget.attrs = {'class': 'form-control', 'placeholder': 'City'}
        self.fields['address_state'].widget.attrs = {'class': 'form-control', 'placeholder': 'State'}
        self.fields['address_state'].choices = statesList.STATE_CHOICES
        self.fields['address_zip'].widget.attrs = {'class': 'form-control', 'placeholder': 'Zip Code'}
        self.fields['home_phone'].widget.attrs = {'class': 'form-control', 'placeholder': '1234567890'}
        self.fields['cell_phone'].widget.attrs = {'class': 'form-control', 'placeholder': '1234567890'}
        self.fields['e_cont_fname'].widget.attrs = {'class': 'form-control', 'placeholder': 'First Name'}
        self.fields['e_cont_lname'].label = 'Emergency Contact - First Name'
        self.fields['e_cont_lname'].widget.attrs = {'class': 'form-control', 'placeholder': 'Last Name'}
        self.fields['e_cont_lname'].label = 'Emergency Contact: Last Name'
        self.fields['e_cont_home_phone'].widget.attrs = {'class': 'form-control', 'placeholder': '1234567890'}
        self.fields['e_cont_home_phone'].label = 'Emergency Contact: Home Phone Number'
        self.fields['e_cont_cell_phone'].widget.attrs = {'class': 'form-control', 'placeholder': '1234567890'}
        self.fields['e_cont_cell_phone'].label = 'Emergency Contact: Cell Phone Number'
        self.fields['primary_doctor'].widget.attrs = {'class': 'form-control', 'placeholder': 'Doctor'}
        self.fields['primary_doctor'].choices = doctor_tuple
        self.fields['primary_doctor'].label = 'Doctor'

    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'address_street', 'address_city', 'address_state', 'address_zip',
                  'home_phone', 'cell_phone', 'e_cont_fname', 'e_cont_lname', 'e_cont_home_phone',
                  'e_cont_cell_phone', 'primary_doctor')

    @classmethod
    def handle_post(cls, user_type, patient, post_data, failedFormDict):
        if user_type == staticHelpers.UserTypes.patient:
            self = UpdatePatient(postData=post_data)
            valid = True

            try:
                patient.home_phone = validate.phone(post_data['home_phone'])
            except forms.ValidationError as e:
                self.add_error('home_phone', e.code)
                valid = False

            try:
                patient.address_zip = validate.zip(post_data['address_zip'])
            except forms.ValidationError as e:
                self.add_error('address_zip', e.code)
                valid = False

            try:
                patient.cell_phone = validate.phone(post_data['cell_phone'])
            except forms.ValidationError as e:
                self.add_error('cell_phone', e.code)
                valid = False

            try:
                patient.e_cont_home_phone = validate.phone(post_data['e_cont_home_phone'])
            except forms.ValidationError as e:
                self.add_error('e_cont_home_phone', e.code)
                valid = False

            try:
                patient.e_cont_cell_phone = validate.phone(post_data['e_cont_cell_phone'])
            except forms.ValidationError as e:
                self.add_error('e_cont_cell_phone', e.code)
                valid = False

            if not valid:
                # Send the validated form back to the user and mark the form's modal to be auto-opened
                failedFormDict["profileForm"] = self
                failedFormDict["autoOpen"] = "updateProfile"
            else:
                # Form is good so save it
                patient.first_name = post_data['first_name']
                patient.last_name = post_data['last_name']
                patient.address_street = post_data['address_street']
                patient.address_city = post_data['address_city']
                patient.address_state = post_data['address_state']
                patient.e_cont_fname = post_data['e_cont_fname']
                patient.e_cont_lname = post_data['e_cont_lname']

                doctor_id = post_data['primary_doctor']
                patient.primary_doctor = Doctor.objects.get(id=doctor_id)

                patient.save()
                LogEntry.log_action(patient.username, "Updated their patient data")