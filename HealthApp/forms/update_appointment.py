from django import forms

from HealthApp.models import Appointment


class SelectAppointment(forms.Form):
    def __init__(self, user):
        super().__init__()
        appointment_tuple = tuple(
            Appointment.objects.all().values_list("id", "start_time").order_by("start_time").filter(
                patient_id=user.userprofile_ptr_id))
        self.fields['appointments'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Hospital'}),
            choices=appointment_tuple,
            label='Appointments')
