from django import forms
from django.forms import ModelForm
from .models import Usuario, Persona

class RegistroUsuario(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
    dni = forms.IntegerField()
    email = forms.EmailField()
    fecha_nac = forms.DateField()
    
    
class PersonaForm(forms.ModelForm):
    model = Persona
    fields = ['nombre', 'apellido', 'contraseña']
    
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
    
class EditarPersona(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'contraseña']
        
class EditarUsuario(ModelForm):
    class Meta:
        model = Usuario
        fields = ['email']
        
            
    
class RegistroAyudante(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
    nombre_usuario = forms.CharField()

class ModificarInterno(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
