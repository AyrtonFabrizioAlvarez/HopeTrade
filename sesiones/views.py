from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from sesiones.models import Persona, Usuario
from datetime import date
import json
# Create your views here.

def signup(request):

    if request.method == "GET":
        print("enviando datos")
    else:
        print(request.POST)
        print("reciebiendo datos")


    return render(request, "signup.html", {
        'formulario': UserCreationForm
    })

def signup_user(request):
    #nombre = request.POST['nombre']
    #apellido = request.POST['apellido']
    #contraseña = request.POST['contraseña']
    #dni = request.POST['dni']
    #email = request.POST['email']
    #fecha_nac = request.POST['fecha_nac']
    #cant_valoraciones = request.POST['cant_valoraciones']
    #reputacion =request.POST['reputacion']
    persona = Persona(nombre="asdasd", apellido="sdddd", contraseña="dddd")
    persona.save()
    usuario = Usuario(dni=11222333, email="a@a.com", fecha_nac=date.today(), cant_valoraciones=0, reputacion=0.0, personaId=persona)
    usuario.save()
    return HttpResponse({usuario.dni})