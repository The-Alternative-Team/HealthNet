# not sure if this works

from django import forms

from HealthApp.models import Prescription
from HealthApp.staticHelpers import set_form_id


class AddPrescription(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        set_form_id(self, "AddPrescription")

        # doctor and date fields are uneditable (when/how are they set?)
        # tuple of patients?
        self.fields['patient'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.username)

        self.fields['drug'].widget.attrs = {'class': 'form-control', 'placeholder': 'Drug Name'}
        self.fields['refills'].widget.attrs = {'class': 'form-control', 'placeholder': 'Refills'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = Prescription
        # should doctor and date not be here
        fields = ['drug', 'patient', 'refills', 'notes']
