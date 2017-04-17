from django import forms
from datetime import datetime

from HealthApp.models import MedInfo, LogEntry
from HealthApp.staticHelpers import set_form_id


class UpdateMedInfo(forms.ModelForm):
    def __init__(self, postData=None, instance=None):
        super().__init__(data=postData, instance=instance)
        self.fields['notes'].required = False

        if instance is not None:
            set_form_id(self, "UpdateMedInfo")

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
    def buildFormDict(cls, all_patients):
        update_med_info_forms = dict()

        for patient in all_patients:
            try:
                medInfoObj = MedInfo.objects.get(patient_id=patient.id)
            except MedInfo.DoesNotExist:
                medInfoObj = MedInfo(patient=patient)
                medInfoObj.save()

            update_med_info_forms[patient.username] = UpdateMedInfo(instance=medInfoObj)

        return update_med_info_forms

    @classmethod
    def handlePost(cls, username, postData):
        form = UpdateMedInfo(postData=postData, instance=MedInfo.objects.get(patient_id=postData['patient']))
        form.instance.time = datetime.now()
        print(form.errors)
        if form.is_valid():
            medInfo = form.save()
            LogEntry.log_action(username, "Updated the medical info for " + str(medInfo.patient))