from django.db import models
from ofrecimientos.models import Ofrecimiento

# Create your models here.
class Intercambio(models.Model):
    estado = models.TextField()
    valoracion1 = models.BooleanField()
    valoracion2 = models.BooleanField()
    ofrecimientoId = models.ForeignKey(Ofrecimiento, on_delete=models.CASCADE)