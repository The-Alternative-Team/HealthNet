"""
Update Appointment form

Django form for updating appointments

=== Fields ===

doctor ------ (CharField) email ID of the doctor associated with the appointment that can only be filled in if
              the user is a nurse.
patient ----- (CharField) email ID of the patient associated with the appointment that can only be filled in if
              the user is not a patient.
start_time -- (DateTimeField) time that the appointment is scheduled to start.
end_time ---- (DateTimeField) time that the appointment is scheduled to end. 
notes ------- (CharField) any notes for the appointment.

=== Methods ===

__init__ --------- Initializes the form.
handle_post ------ Updates appointment given a completed form.

"""

from django import forms

from HealthApp import staticHelpers
from HealthApp.models import Appointment, LogEntry, Patient, Doctor


class UpdateAppointment(forms.ModelForm):
    def __init__(self, user_type):
        super().__init__()
        staticHelpers.set_form_id(self, "UpdateAppointment")

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

    # Handles the submit of both this form and and add appointment form
    @classmethod
    def handle_post(cls, user_type, user, post_data):
        if 'Cancel Appointment' in post_data:
            # Deletion
            Appointment.objects.all().get(id=post_data['event-id-update']).delete()
            LogEntry.log_action(user.username, "Canceled an appointment")
        else:
            # Update or create

            # Get appointment_doctor
            if user_type == staticHelpers.UserTypes.nurse:
                doctor_id = int(post_data['doctor'])
                appointment_doctor = Doctor.objects.all().filter(id=doctor_id)[0]
            elif user_type == staticHelpers.UserTypes.doctor:
                appointment_doctor = user
            else:
                # It's a patient
                appointment_doctor = user.primary_doctor

            # Get appointment_patient
            if user_type == staticHelpers.UserTypes.patient:
                appointment_patient = user
            else:
                patient_id = int(post_data['patient'])
                appointment_patient = Patient.objects.all().filter(id=patient_id)[0]

            if 'event-id-update' in post_data:
                Appointment.objects.get(id=post_data['event-id-update']).update_appointment(
                    hospital=appointment_patient.hospital, doctor=appointment_doctor,
                    patient=appointment_patient, start_time=post_data['start_time'],
                    end_time=post_data['end_time'], notes=post_data['notes'])
                LogEntry.log_action(user.username, "Updated an appointment")
            else:
                appointment = Appointment(hospital=appointment_patient.hospital, doctor=appointment_doctor,
                                          patient=appointment_patient, start_time=post_data['start_time'],
                                          end_time=post_data['end_time'], notes=post_data['notes'])
                appointment.save()
                LogEntry.log_action(user.username, "Created an appointment")