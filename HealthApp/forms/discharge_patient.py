from django import forms
from HealthApp.models import AdmissionLog
from HealthApp.staticHelpers import set_form_id


class DischargePatient(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        set_form_id(self, "DischargePatient")

        self.fields['userMail'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.username)

    class Meta:
        model = AdmissionLog
        fields = ['userMail']
