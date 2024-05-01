from django.db import models
from ofrecimientos.models import Ofrecimiento

# Create your models here.
class Intercambio(models.Model):
    estado = models.TextField()
    ofrecimientoId = models.ForeignKey(Ofrecimiento, on_delete=models.CASCADE)