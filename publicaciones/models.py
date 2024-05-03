from django.db import models
from sesiones.models import Usuario
from listados.models import Categoria

# Create your models here.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    imagen = models.ImageField(blank=True, null=True)
    aceptada = models.BooleanField()
    usuarioId = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    categoriaId = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Comentario(models.Model):
    texto = models.CharField(max_length=160)
    fecha = models.DateTimeField()
    usuarioId = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacionId = models.ForeignKey(Publicacion, on_delete=models.CASCADE)