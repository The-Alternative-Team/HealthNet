"""
Admit Patient form

Django form for admitting patient.

=== Fields ===

userMail -- (CharField) email ID of the patient that is being admitted.
reason ---- (CharField) reason for admission.
hospital -- (ChoiceField) hospital in which the patient is being admitted.

=== Methods ===

__init__ --------- Initializes the form.
handle_post ------ Creates the admission log given a completed form.

"""

from django import forms
from django.utils import timezone

from HealthApp import staticHelpers
from HealthApp.models import Hospital, AdmissionLog, LogEntry


class AdmitPatient(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        staticHelpers.set_form_id(self, "AdmitPatient")
        self.label = "Admit"    # Used to display the correct verb on the UI

        self.fields['userMail'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.username)

        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))
        self.fields['reason'].widget.attrs = {'class': 'form-control', 'placeholder': 'Reason'}
        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=hospital_tuple,
            label='Hospital',
            initial=patient.hospital)

    class Meta:
        model = AdmissionLog
        fields = ['userMail', 'reason', 'hospital']

    @classmethod
    def handle_post(cls, user_type, user, post_data):
        if user_type == staticHelpers.UserTypes.doctor:
            admit_patient = AdmissionLog(userMail=post_data['userMail'], reason=post_data['reason'],
                                         timeAdmitted=timezone.now(), admittedBy=user.username,
                                         hospital=Hospital.objects.get(id=post_data['hospital']),
                                         admitStatus=True)
            admit_patient.save()
            LogEntry.log_action(user.username, "Admitted " + post_data['userMail'])