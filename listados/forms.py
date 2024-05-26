from django import forms
from .models import Categoria
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class AgregarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo']
    
    titulo = forms.CharField(label="titulo", max_length=25, required=True)

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Categoria.objects.filter(titulo=titulo).exclude(estado='eliminada').exists():
            raise forms.ValidationError("El nombre de la categoría ya existe.")
        return titulo

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo']
    
    titulo = forms.CharField(label="titulo", max_length=25, required=True)

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        try:
            id = Categoria.objects.get(titulo=titulo).id
            if Categoria.objects.filter(titulo=titulo).exclude(id=id).exists():
                raise forms.ValidationError("El nombre de la categoría ya existe.")
        except ObjectDoesNotExist:
            if Categoria.objects.filter(titulo=titulo).exists():
                raise forms.ValidationError("El nombre de la categoría ya existe.")
        return titulo