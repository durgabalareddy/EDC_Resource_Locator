from django import forms
from .models import *


class DockerEditForm(forms.ModelForm):
    class Meta:
        model =  dockers
        fields = ['CaseNo','Host','pVersion','Visibilty','Note']