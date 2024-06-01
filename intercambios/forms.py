from django import forms
from django.forms import ModelForm
from .models import Intercambio

class escribir_texto_cancelacion(forms.Form):
    razon = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Razón'
        }),
        label='Razón'
    )

class realizarIntercambio(forms.ModelForm):
    class Meta:
        model = Intercambio
        fields = ('estado','valoracion1','valoracion2','ofrecimientoId')