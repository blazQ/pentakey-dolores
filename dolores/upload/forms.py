from django import forms
from .models import Partitura

class PartituraForm(forms.ModelForm):
    class Meta:
        model = Partitura
        fields = ['titolo', 'foto']
