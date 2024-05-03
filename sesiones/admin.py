from django.contrib import admin
from .models import Persona, Administrador, Ayudante, Usuario
# Register your models here.

admin.site.register(Persona)
admin.site.register(Administrador)
admin.site.register(Ayudante)
admin.site.register(Usuario)