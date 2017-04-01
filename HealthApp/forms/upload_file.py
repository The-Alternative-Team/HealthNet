from django import forms
from HealthApp.models import UploadedFile


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('title', 'file')
