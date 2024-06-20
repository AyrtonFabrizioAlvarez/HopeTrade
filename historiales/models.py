from django.db import models
from publicaciones.models import Publicacion
from intercambios.models import Intercambio

class Historial(models.Model):
    estado = models.CharField(max_length=100)
    fecha = models.DateField()

class PublicacionHistorial(models.Model):
    publicacionId = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    historialId = models.ForeignKey(Historial, on_delete=models.CASCADE)

class IntercambioHistorial(models.Model):
    intercambioId = models.ForeignKey(Intercambio, on_delete=models.CASCADE)
    historialId = models.ForeignKey(Historial, on_delete=models.CASCADE)
