from django import forms
from django.forms import ModelForm
from .models import Usuario, Persona, Ayudante
from django.core.exceptions import ValidationError

class RegistroUsuario(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
    dni = forms.IntegerField()
    email = forms.EmailField()
    fecha_nac = forms.DateField()
    
    
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'contraseña']
    
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
    
    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')
        if len(contraseña) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return contraseña
    
    
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'email', 'fecha_nac']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está en uso.")
        return email


class AyudanteForm(forms.ModelForm):
    class Meta:
        model = Ayudante
        fields = ['nombre_usuario']
    
    nombre_usuario = forms.CharField()

    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data.get('nombre_usuario')
        if Ayudante.objects.filter(nombre_usuario=nombre_usuario).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return nombre_usuario


class EditarPersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'contraseña']

    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
    
    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')
        if len(contraseña) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return contraseña
        
class EditarUsuario(ModelForm):
    class Meta:
        model = Usuario
        fields = ['email']
    
