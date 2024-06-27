from django.db import models
from sesiones.models import Usuario

# Create your models here.
class Donacion(models.Model):
    nombre = models.TextField(blank=True, null=True)
    apellido = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dni = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    usuarioId = models.ForeignKey(Usuario, blank=True, null=True, on_delete=models.CASCADE)

class Donacion_prod(models.Model):
    producto = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    donacionId = models.ForeignKey(Donacion, on_delete=models.CASCADE)

class Donacion_din(models.Model):
    forma_pago = models.TextField()
    monto = models.FloatField()
    donacionId = models.ForeignKey(Donacion, on_delete=models.CASCADE)
