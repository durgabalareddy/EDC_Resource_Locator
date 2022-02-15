from django import forms
from django.forms import ModelChoiceField
from .models import *

class ResourceTypeSelectionForm(forms.ModelForm):
    Resource_Type = forms.ModelChoiceField(queryset=Resource_Type.objects.order_by('resource_type'), initial=0,label='')

    class Meta:
        model = Resource_Type
        fields = ['Resource_Type']


class ScannerEditForm(forms.ModelForm):
    class Meta:
        model =  Resource_Type
        fields = ['resource_type','provider_id','MITI_Scanner','Quick_Links']