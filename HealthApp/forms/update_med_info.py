# not sure if this works

from django import forms

from HealthApp.models import MedInfo
from django.utils import timezone

from HealthApp.staticHelpers import set_form_id


class UpdateMedInfo(forms.ModelForm):
    def __init__(self, patient):
        super().__init__()
        set_form_id(self, "UpdateMedInfo")

        # patient is uneditable
        # time is automatically now (this needs to update tho...)

        self.fields['heart_rate'] = forms.IntegerField(widget=forms.NumberInput(
                                                           attrs={'class': 'form-control',
                                                                  'placeholder': 'Heart Rate'}),
                                                       label='Heart Rate')
        self.fields['systolic_pressure'] = forms.IntegerField(widget=forms.NumberInput(
                                                                  attrs={'class': 'form-control',
                                                                         'placeholder': 'Systolic Pressure'}),
                                                              label='Systolic Pressure')
        self.fields['diastolic_pressure'] = forms.IntegerField(
                                                               widget=forms.NumberInput(
                                                                   attrs={'class': 'form-control',
                                                                          'placeholder': 'Diastolic Pressure'}),
                                                               label='Diastolic Pressure')
        self.fields['body_temp'] = forms.IntegerField(
                                                      widget=forms.NumberInput(
                                                        attrs={'class': 'form-control',
                                                               'placeholder': 'Body Temperature'}),
                                                      label='Body Temperature')
        self.fields['respiratory_rate'] = forms.IntegerField(
                                                             widget=forms.NumberInput(
                                                                 attrs={'class': 'form-control',
                                                                        'placeholder': 'Respiratory Rate'}),
                                                             label='Respiratory Rate')
        self.fields['notes'] = forms.CharField(
                                               widget=forms.TextInput(
                                                   attrs={'class': 'form-control',
                                                          'placeholder': 'Notes'}),
                                               label='Notes')

    class Meta:
        model = MedInfo
        # should patient and time not be here?
        fields = ['heart_rate', 'systolic_pressure', 'diastolic_pressure', 'body_temp',
                  'respiratory_rate', 'notes']


