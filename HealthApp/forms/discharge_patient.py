"""
Discharge form

Django form for discharging patients.

=== Fields ===

userMail -- (CharField) email ID of the patient that is being discharged

=== Methods ===

__init__ --------- Initializes the form.
handle_post ------ Edits the admission log given a completed form.

"""

from django import forms
from django.utils import timezone

from HealthApp import staticHelpers
from HealthApp.models import AdmissionLog, LogEntry


class DischargePatient(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        staticHelpers.set_form_id(self, "DischargePatient")
        self.label = "Discharge"    # Used to display the correct verb on the UI

        self.fields['userMail'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.username)

    class Meta:
        model = AdmissionLog
        fields = ['userMail']

    @classmethod
    def handle_post(cls, user_type, doctor, post_data):
        if user_type == staticHelpers.UserTypes.doctor:
            user_mail = post_data['userMail']
            log_entry = AdmissionLog.objects.all().filter(userMail=user_mail, admitStatus=True)[0]
            log_entry.admitStatus = False
            log_entry.dischargedBy = doctor.username
            log_entry.timeDischarged = timezone.now()
            log_entry.save()
            LogEntry.log_action(doctor.username, "Discharged " + user_mail)