from django import forms

from HealthApp.models import TestFile
from HealthApp.staticHelpers import set_form_id


class UploadForm(forms.ModelForm):
    def __init__(self, test):
        super().__init__()
        set_form_id(self, "UploadForm")

        self.fields['test_id'] = forms.CharField(widget=forms.HiddenInput(), initial=test.id)

    class Meta:
        model = TestFile
        fields = ('title', 'file')
