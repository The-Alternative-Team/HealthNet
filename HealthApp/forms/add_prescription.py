from django import forms

from HealthApp.models import Prescription


class AddPrescription(forms.ModelForm):
    def __init__(self):
        super().__init__()

        #doctor and date fields are uneditable
        self.fields['drug'].widget.attrs = {'class': 'form-control', 'placeholder': 'Drug Name'}
        self.fields['patient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Patient'}
        self.fields['refills'].widget.attrs = {'class': 'form-control', 'placeholder': 'Refills'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = Prescription
        fields = ['drug', 'doctor', 'patient', 'date', 'refills', 'notes']