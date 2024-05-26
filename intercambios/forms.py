from django import forms
from django.forms import ModelForm

class escribir_texto_cancelacion(forms.Form):
    razon = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Razón'
        }),
        label='Razón'
    )