from django import forms

from HealthApp.staticHelpers import set_form_id
from HealthApp.models.Test import Test


class CreateTestForm(forms.ModelForm):
    def __init__(self, testObj):
        super().__init__()
        set_form_id(self, "CreateTestForm")

        self.fields['test_id'] = forms.CharField(widget=forms.HiddenInput(), initial=testObj.id)

    class Meta:
        model = Test
        fields = ['date', 'patient', 'notes']