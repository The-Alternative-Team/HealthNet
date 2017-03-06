from django import forms

from HealthApp import StaticHelpers
from HealthApp.models import Appointment


class AddAppointment(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()

        # Only allow nurses to set custom doctors
        if user_type == StaticHelpers.UserTypes.nurse:
            self.fields['doctor'].widget.attrs = {'class': 'form-control', 'placeholder': 'Doctor'}
        else:
            del self.fields['doctor']

        # Don't allow patients to set a custom patient
        if user_type != StaticHelpers.UserTypes.patient:
            self.fields['patient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Patient'}
        else:
            del self.fields['patient']

        self.fields['start_time'].widget.attrs = {'class': 'form-control',
                                                  'placeholder': 'Start Time: (YYYY-MM-DD HH:MM)'}
        self.fields['end_time'].widget.attrs = {'class': 'form-control', 'placeholder': 'End Time: (YYYY-MM-DD HH:MM)'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'start_time', 'end_time', 'notes']
