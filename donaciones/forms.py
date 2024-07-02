from django import forms
from donaciones.models import Donacion, Donacion_din, Donacion_prod

class DniForm(forms.Form):
    dni = forms.CharField(label='DNI', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))


class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ['dni', 'nombre', 'apellido', 'email']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class DonacionDineroForm(forms.ModelForm):
    FORMA_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('mercado_pago', 'Mercado Pago'),
    ]

    forma_pago = forms.ChoiceField(
        choices=FORMA_PAGO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Donacion_din
        fields = ['forma_pago', 'monto']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DonacionProductoForm(forms.ModelForm):
    class Meta:
        model = Donacion_prod
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
class MercadoPagoForm(forms.ModelForm):
    class Meta:
        model = Donacion_din
        fields = ["monto"]
        labels = {"monto": "Monto a donar"}
        widgets = {
            "monto": forms.NumberInput(
                attrs={
                    "min": "1",
                    "max": "1000000",
                    "step": "1",
                    "class": "form-control",
                }
            ),
        }