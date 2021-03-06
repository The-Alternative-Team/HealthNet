"""
Set Patient Hospital form

Django form for transferring patients.

=== Fields ===

patient_id -- (CharField) email ID of the patient being transferred
hospital ---- (ChoiceField) hospital that the patient is being transferred to

=== Methods ===

__init__ --------- Initializes the form.
build_form_dict -- Creates a dictionary of all the set patient hospital forms for each patient.
handle_post ------ Transfers patient given a completed form.

"""

from django import forms
from HealthApp import staticHelpers
from HealthApp.models import Hospital, Patient, LogEntry, Message


class SetPatientHospital(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        staticHelpers.set_form_id(self, "SetPatientHospital")

        self.fields['patient_id'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.id)

        # Generate hospital ChoiceField
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))

        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=hospital_tuple,
            label='Hospital',
            initial=patient.hospital)

    class Meta:
        model = Patient
        fields = ('hospital',)

    @classmethod
    def build_form_dict(cls, all_patients):
        forms_dict = dict()

        for patient in all_patients:
            forms_dict[patient.username] = SetPatientHospital(patient)

        return forms_dict

    @classmethod
    def handle_post(cls, user_type, doctor, post_data):
        if user_type == staticHelpers.UserTypes.doctor:
            patient_id = post_data['patient_id']
            patient = Patient.objects.all().filter(id=patient_id)[0]

            hospital_id = post_data['hospital']
            patient.hospital = Hospital.objects.all().filter(id=hospital_id)[0]

            patient.save()

            LogEntry.log_action(doctor.username, "Transferred patient " + patient.username + " to " +
                                patient.hospital.name)
            Message.sendNotifMessage(patient.username, "You have been transferred to a new hospital",
                                     "Your new hospital is " + patient.hospital.full_string())