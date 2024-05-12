from django import forms
from listados.models import Categoria
from .models import Publicacion
from .models import Comentario

class RealizarPublicacion(forms.ModelForm):
    categoriaId = forms.ModelChoiceField(queryset=Categoria.objects.all(), 
    widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Publicacion
        fields = ['titulo','descripcion','cantidad','imagen','categoriaId']

    def __init__(self, *args, **kwargs):
        super(RealizarPublicacion, self).__init__(*args, **kwargs)
        # Personalizamos el widget para que muestre el titulo de la categoría
        self.fields['categoriaId'].label_from_instance = lambda obj: "%s" % obj.titulo

class RealizarComentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto',]
