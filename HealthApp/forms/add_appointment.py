"""
Add Appointment form

Django form for adding appointments.

=== Fields ===

doctor ------ (CharField) email ID of the doctor associated with the appointment that can only be filled in if
              the user is a nurse.
patient ----- (CharField) email ID of the patient associated with the appointment that can only be filled in if
              the user is not a patient.
start_time -- (DateTimeField) time that the appointment is scheduled to start.
end_time ---- (DateTimeField) time that the appointment is scheduled to end. 
notes ------- (CharField) any notes for the appointment.

=== Methods ===

__init__ ---- Initializes the form.

"""

from django import forms

from HealthApp import staticHelpers
from HealthApp.models import Appointment
from HealthApp.staticHelpers import set_form_id


class AddAppointment(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()
        set_form_id(self, "AddAppointment")

        # Only allow nurses to set custom doctors
        if user_type == staticHelpers.UserTypes.nurse:
            self.fields['doctor'].widget.attrs = {'class': 'form-control', 'placeholder': 'Doctor'}
        else:
            del self.fields['doctor']

        # Don't allow patients to set a custom patient
        if user_type != staticHelpers.UserTypes.patient:
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
