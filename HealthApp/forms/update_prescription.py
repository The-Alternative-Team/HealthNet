# not sure if this works

from django import forms
from django.utils import timezone

from HealthApp.models import Prescription


class AddPrescription(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()

        # doctor and date fields are uneditable (when/how are they set?)
        # patient not changed
        # date needs to update

        self.fields['date'] = timezone.now()

        self.fields['drug'] = forms.CharField(initial=patient.prescription.drug,
                                              widget=forms.TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Drug Name'}),
                                              label='Drug Name')

        self.fields['refills'] = forms.IntegerField(initial=patient.prescription.refills,
                                                    widget=forms.TextInput(
                                                        attrs={'class': 'form-control', 'placeholder': 'Refills'}),
                                                    label='Refills')

        self.fields['notes'] = forms.CharField(initial=patient.prescription.notes,
                                               widget=forms.TextInput(
                                                   attrs={'class': 'form-control', 'placeholder': 'Notes'}),
                                               label='Notes')

    class Meta:
        model = Prescription
        # should doctor, patient, and date not be here?
        fields = ['drug', 'doctor', 'patient', 'date', 'refills', 'notes']