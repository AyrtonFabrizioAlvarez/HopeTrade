from django import forms
from .models import Categoria
from django.core.exceptions import ValidationError

class AgregarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo']
    
    titulo = forms.CharField(label="titulo", max_length=25, required=True)

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Categoria.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError("El nombre de la categoría ya existe.")
        return titulo

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo']
    
    titulo = forms.CharField(label="titulo", max_length=25, required=True)

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Categoria.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError("El nombre de la categoría ya existe.")
        return titulo