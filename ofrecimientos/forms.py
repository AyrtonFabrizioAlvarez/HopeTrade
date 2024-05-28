from django import forms
from .models import Ofrecimiento
from .models import Sucursal
from listados.models import Categoria
from django.utils import timezone

class RealizarOfrecimiento(forms.ModelForm):
    class Meta:
        model = Ofrecimiento
        fields = ('fecha','articulo', 'cantidad', 'descripcion', 'imagen', 'categoriaId', 'sucursalId')
    
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'placeholder': 'dd/mm/aaaa HH:MM', 'class': 'form-control'}),
        input_formats=['%d/%m/%Y %H:%M']
    )
    categoriaId = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sucursalId = forms.ModelChoiceField(
        queryset=Sucursal.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RealizarOfrecimiento, self).__init__(*args, **kwargs)
        self.fields['categoriaId'].label_from_instance = lambda obj: "%s" % obj.titulo
        self.fields['sucursalId'].label_from_instance = lambda obj: "%s" % obj.nombre

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        # Verificar si la fecha es posterior al día actual
        if fecha <= timezone.now():
            raise forms.ValidationError("Ingrese una fecha válida.")
        # Verificar si la fecha está entre lunes y viernes
        if fecha.weekday() > 4:  # 0 = lunes, 4 = viernes
            raise forms.ValidationError("Ingresar un día entre lunes y viernes.")
        # Verificar si la hora está entre 8:00 y 20:00
        if fecha.hour < 8 or fecha.hour >= 20:
            raise forms.ValidationError("Ingresar un horario entre las 08:00 y las 20:00.")
        return fecha
    
class escribir_texto_cancelacion(forms.Form):
    texto = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ej: sucursal muy lejana'
        }),
        label='Razón'
    )
