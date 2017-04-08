# not sure if this works

from django import forms

from HealthApp.models import MedInfo


class AddMedInfo(forms.ModelForm):
    def __init__(self):
        super.__init__()

        # patient is uneditable (when are these set?)
        # time is automatically now
        self.fields['patient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Patient'}
        self.fields['heart_rate'].widget.attrs = {'class': 'form-control', 'placeholder': 'Heart Rate'}
        self.fields['systolic_pressure'].widget.attrs = {'class': 'systolic_pressure', 'placeholder': 'Systolic Pressure'}
        self.fields['diastolic_pressure'].widget.attrs = {'class': 'diastolic_pressure', 'placeholder': 'Diastolic Pressure'}
        self.fields['body_temp'].widget.attrs = {'class': 'body_temp', 'placeholder': 'Body Temperature'}
        self.fields['respiratory_rate'].widget.attrs = {'class': 'respiratory_rate', 'placeholder': 'Respiratory Rate'}
        self.fields['notes'].widget.attrs = {'class': 'notes', 'placeholder': 'Notes'}

    class Meta:
        model = MedInfo
        #should time not be here?
        fields = ['patient', 'time', 'heart_rate', 'systolic_pressure', 'diastolic_pressure', 'body_temp',
                  'respiratory_rate', 'notes']


