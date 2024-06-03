from django import forms
from .models import Categoria
from publicaciones.models import Publicacion
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
    
    titulo = forms.CharField(label="titulo", max_length=25)

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Categoria.objects.filter(titulo=titulo).exclude(estado='eliminada').exists():
            raise forms.ValidationError("El nombre de la categoría ya existe.")
        else:
            try:
                categoria = Categoria.objects.get(titulo=titulo)
                if Publicacion.objects.filter(categoriaId=categoria).exclude(estado="eliminada").exists():
                    raise forms.ValidationError("El nombre al que usted quiere cambiar pertenece a una categoría eliminada que aún posee publicaciones")
                else:
                    categoria.delete()
            except ObjectDoesNotExist:
                None
        return titulo