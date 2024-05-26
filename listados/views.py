from django.shortcuts import render, redirect, get_object_or_404
from .forms import AgregarCategoriaForm, EditarCategoriaForm
from listados.models import Categoria
from django.contrib import messages
from intercambios.models import Intercambio
from ofrecimientos.models import Ofrecimiento
from datetime import datetime

from django.utils import timezone

def agregar_categoria(request):
    if request.method == 'POST':
        categoria_form = AgregarCategoriaForm(request.POST)
        if categoria_form.is_valid():
            categoria = categoria_form.save(commit=False)
            categoria.estado = 'disponible'
            categoria.save()
            messages.success(request, "La categoría se creó exitosamente")
            return redirect('/listados/listar_categorias')
    else:
        categoria_form = AgregarCategoriaForm()
    
    return render(request, 'listados/agregar_categoria.html', {'form_categoria': categoria_form})

def listar_categorias(request):
    categorias = Categoria.objects.all().exclude(estado='eliminada')
    return render(request, "listados/listar_categorias.html", {'categorias': categorias})

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    categoria_form = EditarCategoriaForm(instance=categoria)
    if request.method == 'POST':
        nueva_categoria_form = EditarCategoriaForm(request.POST)
        if nueva_categoria_form.is_valid():
            categoria = categoria_form.save(commit=False)
            categoria.titulo = request.POST['titulo']
            categoria.save()
            return redirect('/listados/listar_categorias')
        else:
            categoria_form = nueva_categoria_form
    
    return render(request, 'listados/editar_categoria.html',{'form_categoria':categoria_form})

def eliminar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    if request.method == 'GET':
        if Categoria.objects.count() > 1:
            return render(request, 'listados/eliminar_categoria.html', {'categoria':categoria})
        else:
            messages.warning(request, "No se puede eliminar la categoría, tiene que existir al menos una en el sistema")
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "confirm":
            messages.success(request, 'Se eliminó la categoría exitosamente')
            categoria.estado = 'eliminada'
            categoria.save()

    return redirect('/listados/listar_categorias')

def list_exchanges_today(request):
    hoy = timezone.now().date()
    intercambios_hoy = Intercambio.objects.filter(ofrecimientoId__fecha__date=hoy).filter(estado = "pendiente")
    return render(request, "intercambios/intercambios_del_dia.html", {"intercambios_hoy": intercambios_hoy})

