from django import forms

from HealthApp.models import TestFile
from HealthApp.staticHelpers import set_form_id


class UploadForm(forms.ModelForm):
    def __init__(self, postData=None, files=None, test=None):
        super().__init__(data=postData, files=files)

        if test is not None:
            set_form_id(self, "UploadForm")

            self.fields['title'].widget.attrs = {'class': 'form-control', 'placeholder': 'Title'}
            self.fields['file'].widget.attrs = {'class': 'btn btn-default'}
            self.fields['test'].widget = forms.HiddenInput()
            self.fields['test'].initial = test

    class Meta:
        model = TestFile
        fields = ('title', 'file', 'test')
