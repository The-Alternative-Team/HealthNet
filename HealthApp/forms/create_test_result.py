"""
Create Test Result form

Django form for creating test results.

=== Fields ===

test_id -------- (CharField) ID of the test associated with the test result.
date ----------- (DateTimeField) date that the test was entered.
patient -------- (CharField) email ID of the patient associated with the test.
notes ---------- (CharField) notes that the doctor enters.
releaseStatus -- (BooleanField) boolean that shows whether the patient can view the test.

=== Methods ===

__init__ -- Initializes the form.

"""

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
        self.fields['releaseStatus'].label = 'Release to patient?'

    class Meta:
        model = Test
        fields = ['date', 'patient', 'notes', 'releaseStatus']