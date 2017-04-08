from django import forms

from HealthApp.models import Hospital, Patient


class SetPatientHospital(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()

        self.fields['patient_id'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'aria-hidden': 'true'}),
            initial=patient.id)

        # Generate hospital ChoiceField
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))

        self.fields['hospital'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'State'}),
            choices=hospital_tuple,
            label='Hospital',
            initial=patient.hospital)

    class Meta:
        model = Patient
        fields = ('hospital',)