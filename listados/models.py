from django.db import models

# Create your models here.
class Categoria(models.Model):
    titulo = models.TextField()
    estado = models.TextField()