# not sure if this works

from django import forms

from HealthApp.models import MedInfo
from django.utils import timezone


class AddPrescription(forms.ModelForm):
    def __init__(self, patient):
        super.__init__()

        # patient is uneditable
        # time is automatically now (this needs to update tho...)

        self.fields['time'] = timezone.now()

        self.fields['heart_rate'] = forms.IntegerField(initial=patient.MedInfo.heart_rate,
                                                       widget=forms.TextInput(
                                                           attrs={'class': 'form-control',
                                                                  'placeholder': 'Heart Rate'}),
                                                       label='Heart Rate')
        self.fields['systolic_pressure'] = forms.IntegerField(initial=patient.MedInfo.systolic_pressure,
                                                              widget=forms.TextInput(
                                                                  attrs={'class': 'systolic_pressure',
                                                                         'placeholder': 'Systolic Pressure'}),
                                                              label='Systolic Pressure')
        self.fields['diastolic_pressure'] = forms.IntegerField(initial=patient.MedInfo.diastolic_pressure,
                                                               widget=forms.TextInput(
                                                                   attrs={'class': 'diastolic_pressure',
                                                                          'placeholder': 'Diastolic Pressure'}),
                                                               label='Diastolic Pressure')
        self.fields['body_temp'] = forms.IntegerField(initial=patient.MedInfo.body_temp,
                                                      widget=forms.TextInput(
                                                        attrs={'class': 'body_temp',
                                                               'placeholder': 'Body Temperature'}),
                                                      label='Body Temperature')
        self.fields['respiratory_rate'] = forms.IntegerField(initial=patient.MedInfo.respiratory_rate,
                                                             widget=forms.TextInput(
                                                                 attrs={'class': 'respiratory_rate',
                                                                        'placeholder': 'Respiratory Rate'}),
                                                             label='Respiratory Rate')
        self.fields['notes'] = forms.CharField(initial=patient.MedInfo.notes,
                                               widget=forms.TextInput(
                                                   attrs={'class': 'notes',
                                                          'placeholder': 'Notes'}),
                                               label='Notes')

    class Meta:
        model = MedInfo
        # should patient and time not be here?
        fields = ['patient', 'time', 'heart_rate', 'systolic_pressure', 'diastolic_pressure', 'body_temp',
                  'respiratory_rate', 'notes']


