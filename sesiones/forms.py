from django import forms

class RegistroUsuario(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    
