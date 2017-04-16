from django import forms
from HealthApp.models import Hospital, AdmissionLog, Patient
from HealthApp.staticHelpers import set_form_id


class AdmitPatient(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        set_form_id(self, "AdmitPatient")
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))

        self.fields['userMail'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.username)

        self.fields['reason'].widget.attrs = {'class': 'form-control', 'placeholder': 'Reason'}
        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=hospital_tuple,
            label='Hospital',
            initial=patient.hospital)

    class Meta:
        model = AdmissionLog
        fields = ['userMail', 'reason', 'hospital']
