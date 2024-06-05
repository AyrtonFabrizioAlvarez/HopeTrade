from django.shortcuts import render, redirect
from django.contrib import messages
from publicaciones.models import Publicacion
from publicaciones.models import Comentario
from ofrecimientos.models import Ofrecimiento
from listados.models import Categoria
from sesiones.models import Usuario
from .forms import RealizarPublicacion
from .forms import RealizarComentario
from datetime import datetime
import base64

# Create your views here.
def realizar_publicacion(request):
    if request.method == "POST":    
        realizar_publicacion_form = RealizarPublicacion(request.POST, request.FILES)
        if realizar_publicacion_form.is_valid():
            try:
                publicacion = realizar_publicacion_form.save(commit=False)
                usuarioId = request.session.get('rol_id')
                publicacion.usuarioId = Usuario.objects.get(id=usuarioId) #hay que modificar el user
                if Publicacion.objects.filter(titulo=publicacion.titulo, usuarioId=publicacion.usuarioId).exclude(estado="eliminada").exclude(estado="finalizada").exists():
                    return render(request, "publicaciones/realizar_publicacion.html", {
                    'form': RealizarPublicacion(),
                    "error": 'No se pudo realizar la publicación, actualmente ya posee una publicación con el mismo título'
                })  
                publicacion.categoria_id = realizar_publicacion_form.cleaned_data['categoriaId'].id
                publicacion.estado = "disponible"
                imagen=(
                    base64.b64encode(realizar_publicacion_form.cleaned_data["imagen"].read())
                    if realizar_publicacion_form.cleaned_data["imagen"]
                    else realizar_publicacion_form.cleaned_data["imagen"]
                )
                publicacion.imagen = imagen
                publicacion.save()
                messages.success(request, "Su publicacion se creó exitosamente")
                ruta = "/publicaciones/listar_publicaciones_usuario/" + str(request.session['rol_id'])
                return redirect(ruta)
            except:
                return render(request, "publicaciones/realizar_publicacion.html", {
                    'form': RealizarPublicacion(),
                    "error": 'algo salió mal'
                })  
    else:
        realizar_publicacion_form = RealizarPublicacion()
    return render(request, "publicaciones/realizar_publicacion.html", {
        'form': RealizarPublicacion()
    })

def cancelar_operacion(request):
    return redirect('publicaciones:listar_publicaciones_sistema')

def realizar_comentario(request, publicacion_id):
    if request.method == "POST":
        realizar_comentario_form = RealizarComentario(request.POST)
        if realizar_comentario_form.is_valid():
            try:
                comentario = realizar_comentario_form.save(commit=False)
                comentario.fecha = datetime.now()
                usuarioId = request.session.get('rol_id')
                comentario.usuarioId = Usuario.objects.get(id=usuarioId)
                comentario.publicacionId = Publicacion.objects.get(id=publicacion_id) 
                comentario.save()
                ruta = "/publicaciones/seleccionar_publicacion/" + str(publicacion_id)
                return redirect(ruta)
            except:
                return render(request, "publicaciones/realizar_comentario.html", {
                    'form': RealizarComentario(),
                    "error": 'algo salió mal'
                })
    return render(request, "publicaciones/realizar_comentario.html", {
        'form': RealizarComentario()
    })

def listar_publicaciones_sistema(request):
    publicacionesSistema = Publicacion.objects.all()
    if request.session['rol'] != 'administrador':
        publicacionesSistema = Publicacion.objects.all().exclude(estado='eliminada').exclude(estado='aceptada').exclude(estado="finalizada")
    categorias = Categoria.objects.all()
    categorias_eliminadas = Categoria.objects.filter(estado='eliminada')
    for cat in categorias_eliminadas:
        if not publicacionesSistema.filter(categoriaId=cat).exists():
            categorias.exclude(id=cat.id)
    if len(publicacionesSistema) == 0:
        messages.warning(request, 'No existen publicaciones en el sistema')
    return render(request, "publicaciones/listar_publicaciones_sistema.html", {
        'publicacionesSistema': publicacionesSistema,
        'categorias': categorias,
    })


def listar_publicaciones_usuario(request, user_id):
    usuario = Usuario.objects.get(id=user_id)
    publicacionesUsuario = Publicacion.objects.filter(usuarioId=usuario).exclude(estado='eliminada').exclude(estado='aceptada').exclude(estado="finalizada")
    categorias = Categoria.objects.all()
    categorias_eliminadas = Categoria.objects.filter(estado='eliminada')
    for cat in categorias_eliminadas:
        if not publicacionesUsuario.filter(categoriaId=cat).exists():
            categorias.exclude(id=cat.id)
    if len(publicacionesUsuario) == 0:
        messages.warning(request, 'No existen publicaciones del usuario')
    return render(request, "publicaciones/listar_publicaciones_usuario.html", {
        'publicacionesUsuario': publicacionesUsuario,
        'categorias': categorias,
    })  

def seleccionar_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    comentarios = Comentario.objects.filter(publicacionId=publicacion_id)
    if bool(publicacion.imagen):
        publicacion_imagen = publicacion.imagen.decode("utf-8")
    else:
        publicacion_imagen = None
    return render(request, 'publicaciones/seleccionar_publicacion.html', {'publicacion': publicacion, 'comentarios': comentarios, 'publicacion_imagen': publicacion_imagen})

def eliminar_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    if request.method == "POST":
        ofrecimientos = Ofrecimiento.objects.filter(publicacionId=publicacion_id).exclude(estado='eliminado')
        if not ofrecimientos:
            publicacion.estado = 'eliminada'
            publicacion.save()
            messages.success(request, "La publicación se eliminó exitosamente")
        else:
            messages.warning(request, "No se puede eliminar una publicación con ofrecimientos pendientes")
        if request.session['rol'] == 'usuario':
            ruta = "/publicaciones/listar_publicaciones_usuario/" + str(request.session['rol_id'])
        else:
            ruta = "/publicaciones/listar_publicaciones_sistema"
        return redirect(ruta)
    return render(request, 'publicaciones/eliminar_publicacion.html', { 'publicacion': publicacion })

def filtrar_publicaciones_sistema(request):
    publicaciones = Publicacion.objects.all()
    if request.session['rol'] != 'administrador':
        publicaciones = Publicacion.objects.all().exclude(estado='eliminada').exclude(estado='aceptada').exclude(estado="finalizada")
    categorias = Categoria.objects.all()
    categorias_eliminadas = Categoria.objects.filter(estado='eliminada')
    for cat in categorias_eliminadas:
        if not publicaciones.filter(categoriaId=cat).exists():
            categorias.exclude(id=cat.id)
    categoria = request.POST.get('categoria')
    reputacion = request.POST.get('reputacion')
    estado = request.POST.get('estado')
    categoria_seleccionada = None
    estado_seleccionado = None
    reputacion_seleccionada=None
    if categoria != 'Categoria':
        if categoria.isdigit():
            publicaciones = publicaciones.filter(categoriaId__id=categoria)
            categoria_seleccionada = Categoria.objects.get(id=categoria)
        else:
            categoria_seleccionada = Categoria.objects.get(titulo=categoria)
            publicaciones = publicaciones.filter(categoriaId__id=categoria_seleccionada.id)
    if reputacion is not None and reputacion != 'Reputacion':
        reputacion_int = int(reputacion)
        #traigo las publicaciones con reputacion >= a lo que pide el filtro y < lo que pide el filtro +1
        publicaciones = publicaciones.filter(usuarioId__reputacion__gte=reputacion_int, usuarioId__reputacion__lt=reputacion_int + 1)
        reputacion_seleccionada = reputacion
    if estado != 'Estado' and estado != None:
        publicaciones = publicaciones.filter(estado=estado)
        estado_seleccionado = estado
    if len(publicaciones) == 0:
        messages.warning(request, f'No existen publicaciones para el filtro seleccionado')
    return render(request, "publicaciones/listar_publicaciones_sistema.html", {
        'publicacionesSistema': publicaciones,
        'categorias': categorias,
        'categoria_seleccionada':categoria_seleccionada,
        'reputacion_seleccionada':reputacion_seleccionada,
        'estado_seleccionado':estado_seleccionado
    })
    
def filtrar_publicaciones_usuario(request):
    usuario = Usuario.objects.get(id=request.session['rol_id'])
    publicaciones = Publicacion.objects.filter(usuarioId=usuario).exclude(estado='eliminada').exclude(estado="finalizada")
    categorias = Categoria.objects.all()
    categorias_eliminadas = Categoria.objects.filter(estado='eliminada')
    categoria_seleccionada = None
    for cat in categorias_eliminadas:
        if not publicaciones.filter(categoriaId=cat).exists():
            categorias.exclude(id=cat.id)
    categoria = request.POST.get('categoria')
    if categoria != 'Categoria':
        if categoria.isdigit():
            publicaciones = publicaciones.filter(categoriaId__id=categoria)
            categoria_seleccionada = Categoria.objects.get(id=categoria)
        else:
            categoria_seleccionada = Categoria.objects.get(titulo=categoria)
            publicaciones = publicaciones.filter(categoriaId__id=categoria_seleccionada.id)
    if len(publicaciones) == 0:
        messages.warning(request, f'No existen publicaciones para el filtro seleccionado')
    return render(request, "publicaciones/listar_publicaciones_usuario.html", {
        'publicacionesUsuario': publicaciones,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada
    })