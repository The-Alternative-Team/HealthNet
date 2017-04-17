from django import forms
from django.utils import timezone

from HealthApp.models import Prescription, LogEntry, Patient
from HealthApp import staticHelpers


class AddPrescription(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        staticHelpers.set_form_id(self, "AddPrescription")
        
        self.fields['patient'] = forms.CharField(widget=forms.HiddenInput(), initial=patient.username)

        self.fields['drug'].widget.attrs = {'class': 'form-control', 'placeholder': 'Drug Name'}
        self.fields['refills'].widget.attrs = {'class': 'form-control', 'placeholder': 'Refills'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = Prescription
        fields = ['drug', 'patient', 'refills', 'notes']

    @classmethod
    def build_form_dict(cls, all_patients):
        forms_dict = dict()

        for patient in all_patients:
            forms_dict[patient.username] = AddPrescription(patient)

        return forms_dict

    @classmethod
    def handle_post(cls, user_type, doctor, post_data):
        if user_type == staticHelpers.UserTypes.doctor:
            prescription = Prescription(drug=post_data['drug'], doctor=doctor,
                                        patient=Patient.objects.get(username=post_data['patient']),
                                        date=timezone.now(), refills=post_data['refills'],
                                        notes=post_data['notes'])
            prescription.save()
            LogEntry.log_action(doctor.username, "Added prescription for " + post_data['patient'])