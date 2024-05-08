"""
URL configuration for hopetrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from intercambios import views as intercambios
from sesiones import views as sesiones

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', intercambios.listar_intercambios),
    path('intercambios/<str:prueba>', intercambios.prueba),
    #REGISTRAR USUARIO
    path('signup/', sesiones.signup, name='signup'),
    path('signup_user/', sesiones.signup_user, name='signup_user')
]
