from django import forms
from django.forms import ModelForm
from .models import Usuario, Persona, Ayudante
from django.core.exceptions import ValidationError
import re
from django.utils import timezone




class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'contraseña']
        
    nombre = forms.CharField(label="nombre", max_length=25, required=True)
    apellido = forms.CharField(label="apellido", max_length=25, required=True)
    contraseña = forms.CharField()

    
    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')
         # Expresión regular para verificar si la contraseña cumple con los requisitos
        patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$"
        # Verificar si la contraseña coincide con el patrón
        if re.match(patron, contraseña):
            return contraseña
        else:
            raise forms.ValidationError("La contraseña debe contener al menos 8 caracteres, una mayuscula, una minuscula, un caracter especial y un numero")
    
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'email', 'fecha_nac']
        widgets = {'fecha_nac': forms.DateInput(attrs={'class':'datepicker'})}
        
    dni = forms.IntegerField()
    email = forms.EmailField()
    fecha_nac = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}), input_formats=['%d/%m/%Y'])

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError("DNI ya existente, ingrese otro por favor.")
        elif dni < 1000000:
            raise forms.ValidationError("Ingrese un DNI válido.")
        return dni
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ya existente, ingrese otro por favor.")
        return email
    
    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data.get('fecha_nac')
        if fecha_nac:
            edad = timezone.now().date().year - fecha_nac.year
            if (timezone.now().date().month, timezone.now().date().day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1  # Ajuste si aún no ha cumplido años en este año
            if edad < 18:
                raise ValidationError("Debe ser mayor de edad para registrarse.")
        return fecha_nac

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
         # Expresión regular para verificar si la contraseña cumple con los requisitos
        patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$"
        # Verificar si la contraseña coincide con el patrón
        if re.match(patron, contraseña):
            return contraseña
        else:
            raise forms.ValidationError("La contraseña debe contener: ( >=8 caracteres, una mayuscula, una minuscula, un numero, un caracter especial)")
        
class EditarUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'dni', 'fecha_nac']
        
    email = forms.EmailField()
    dni = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_nac = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exclude(dni=self.data['dni']).exists():
            raise forms.ValidationError("El email que desea ingresar ya se encuentra registrado en el sistema.")
        return email
            
