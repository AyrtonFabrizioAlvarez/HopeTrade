from django.db import models

# Create your models here.

class Persona(models.Model):
    nombre = models.TextField()
    apellido = models.TextField()
    contraseña = models.TextField()

class Administrador(models.Model):
    nombre_usuario = models.TextField()
    personaId = models.ForeignKey(Persona, on_delete=models.CASCADE)

class Ayudante(models.Model):
    nombre_usuario = models.TextField()
    personaId = models.ForeignKey(Persona, on_delete=models.CASCADE)

class Usuario(models.Model):
    dni = models.BigIntegerField()
    email = models.EmailField()
    fecha_nac = models.DateField()
    reputacion = models.FloatField()
    cant_valoraciones = models.IntegerField()
    personaId = models.ForeignKey(Persona, on_delete=models.CASCADE)