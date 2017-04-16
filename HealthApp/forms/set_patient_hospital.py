from django import forms

from HealthApp.models import Hospital, Patient
from HealthApp.staticHelpers import set_form_id


class SetPatientHospital(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        set_form_id(self, "SetPatientHospital")

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
