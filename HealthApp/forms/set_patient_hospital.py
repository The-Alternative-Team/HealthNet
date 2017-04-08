from django import forms

from HealthApp.models import Hospital


class SetPatientHospital(forms.BaseForm):
    def __init__(self):
        super().__init__()

        self.fields['patient_id'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'aria-hidden': 'true'}))

        # Generate hospital ChoiceField
        hospital_tuple = tuple(Hospital.objects.all().values_list("id", "name").order_by("name"))

        self.fields['hospital_id'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'State'}),
            choices=hospital_tuple,
            label='Hospital')