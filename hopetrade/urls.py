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
    path('', intercambios.ver_landing_page),
    path('intercambios/', intercambios.listar_intercambios),
    #SESIONES
    path('signup/', sesiones.signup),
    path('signup_helper/', sesiones.signup_helper),
    path('users/', sesiones.list_users),
    path('helpers/', sesiones.list_helpers),
    path('edit_user/<int:user_id>/', sesiones.edit_user, name='edit_user'),
    path('edit_intern/<int:helper_id>', sesiones.edit_intern, name='edit_intern'),
    path('delete_helper/<int:helper_id>', sesiones.delete_helper, name='delete_helper'),
    
    #EJEMPLO CON PARAMETROS
    path('intercambios2/<str:prueba>', intercambios.prueba),
]
