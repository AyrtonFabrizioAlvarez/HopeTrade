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
    
<<<<<<< Updated upstream
class EditarPersona(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'contraseña']
        
class EditarUsuario(ModelForm):
    class Meta:
        model = Usuario
        fields = ['email']
    
=======
class RegistroAyudante(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
    nombre_usuario = forms.CharField()

class ModificarInterno(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=25)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()
>>>>>>> Stashed changes
