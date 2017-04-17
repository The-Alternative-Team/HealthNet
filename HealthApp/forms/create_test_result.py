from django import forms

from HealthApp.models.Test import Test
from HealthApp.staticHelpers import set_form_id


class CreateTestForm(forms.ModelForm):
    def __init__(self, testObj):
        super().__init__(instance=testObj)
        set_form_id(self, "CreateTestForm")

        self.fields['test_id'] = forms.CharField(widget=forms.HiddenInput(), initial=testObj.id)
        self.fields['date'].widget.attrs = {'class': 'form-control', 'placeholder': 'Date'}
        self.fields['patient'].widget.attrs = {'class': 'form-control', 'placeholder': 'Patient'}
        self.fields['notes'].widget.attrs = {'class': 'form-control', 'placeholder': 'Notes'}

    class Meta:
        model = Test
        fields = ['date', 'patient', 'notes']