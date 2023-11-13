from django import forms
from .models import Spartito

class SpartitoForm(forms.ModelForm):
    class Meta:
        model = Spartito
        fields = ['spartito_image']
