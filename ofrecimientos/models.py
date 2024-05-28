from django.db import models
from listados.models import Categoria
from sesiones.models import Usuario
from publicaciones.models import Publicacion

# Create your models here.
class Sucursal(models.Model):
    nombre = models.TextField()
    ubicacion = models.CharField(max_length=100)

class Ofrecimiento(models.Model):
    fecha = models.DateTimeField()
    articulo = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    imagen = models.BinaryField(null=True, blank=True, editable=True)
    usuarioId = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    categoriaId = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    sucursalId = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    publicacionId = models.ForeignKey(Publicacion, on_delete=models.CASCADE)