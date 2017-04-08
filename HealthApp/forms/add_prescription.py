# not sure if this works

from django import forms

from HealthApp.models import Prescription, Patient


class AddPrescription(forms.ModelForm):
    def __init__(self):
        super().__init__()

        # doctor and date fields are uneditable (when/how are they set?)
        # tuple of patients?

        self.fields['patient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Patient'}
        self.fields['drug'].widget.attrs = {'class': 'form-control', 'placeholder': 'Drug Name'}
        self.fields['refills'].widget.attrs = {'class': 'form-control', 'placeholder': 'Refills'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}



    class Meta:
        model = Prescription
        # should doctor and date not be here
        fields = ['drug', 'doctor', 'patient', 'date', 'refills', 'notes']