from django import forms
from datetime import datetime

from HealthApp.models import MedInfo, LogEntry
from HealthApp import staticHelpers


class UpdateMedInfo(forms.ModelForm):
    def __init__(self, postData=None, instance=None):
        super().__init__(data=postData, instance=instance)
        self.fields['notes'].required = False

        if instance is not None:
            staticHelpers.set_form_id(self, "UpdateMedInfo")

            self.fields['patient'].widget = forms.HiddenInput()
            self.fields['patient'].initial = instance.patient
            self.fields['heart_rate'].widget.attrs = {'class': 'form-control', 'placeholder': 'Heart Rate'}
            self.fields['systolic_pressure'].widget.attrs = {'class': 'form-control', 'placeholder': 'Systolic Pressure'}
            self.fields['diastolic_pressure'].widget.attrs = {'class': 'form-control', 'placeholder': 'Diastolic Pressure'}
            self.fields['body_temp'].widget.attrs = {'class': 'form-control', 'placeholder': 'Body Temperature'}
            self.fields['respiratory_rate'].widget.attrs = {'class': 'form-control', 'placeholder': 'Respiratory Rate'}
            self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = MedInfo
        fields = ['patient', 'heart_rate', 'systolic_pressure', 'diastolic_pressure', 'body_temp', 'respiratory_rate',
                  'notes']

    @classmethod
    def build_form_dict(cls, all_patients):
        forms_dict = dict()

        for patient in all_patients:
            try:
                medInfoObj = MedInfo.objects.get(patient_id=patient.id)
            except MedInfo.DoesNotExist:
                medInfoObj = MedInfo(patient=patient)
                medInfoObj.save()

            forms_dict[patient.username] = UpdateMedInfo(instance=medInfoObj)

        return forms_dict

    @classmethod
    def handle_post(cls, user_type, user, post_data):
        if user_type == staticHelpers.UserTypes.doctor or user_type == staticHelpers.UserTypes.nurse:
            form = UpdateMedInfo(postData=post_data, instance=MedInfo.objects.get(patient_id=post_data['patient']))
            form.instance.time = datetime.now()
            print(form.errors)
            if form.is_valid():
                medInfo = form.save()
                LogEntry.log_action(user.username, "Updated the medical info for " + str(medInfo.patient))