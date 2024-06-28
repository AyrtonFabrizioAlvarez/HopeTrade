from django.shortcuts import render, redirect
from donaciones.models import Donacion, Donacion_din
from sesiones.models import Usuario
from .forms import DniForm, DonacionDineroForm, DonacionForm, DonacionProductoForm, MercadoPagoForm
from .mercadopago import mp, create_preference

# Create your views here.
def ingresar_dni(request):
    if request.method == "POST":
        form = DniForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                usuario = Usuario.objects.get(dni=dni)
                # Redirigir a la vista de donación con el usuario existente
                return redirect('donaciones:completar_donacion_existente', usuario_id=usuario.id)
            except Usuario.DoesNotExist:
                # Redirigir a la vista de completar datos manualmente
                return redirect('donaciones:completar_donacion_manual', dni=dni)
    else:
        form = DniForm()
    return render(request, 'donaciones/ingresar_dni.html', {'form': form})

def completar_donacion_existente(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == "POST":
        donacion = Donacion(usuarioId=usuario)
        donacion.save()
        return redirect('donaciones:seleccionar_tipo_donacion', donacion_id=donacion.id)
    return render(request, 'donaciones/completar_donacion_existente.html', {'usuario': usuario})

def completar_donacion_manual(request, dni):
    if request.method == "POST":
        form = DonacionForm(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.dni = dni
            donacion.save()
            return redirect('donaciones:seleccionar_tipo_donacion', donacion_id=donacion.id)
    else:
        form = DonacionForm(initial={'dni': dni})
    return render(request, 'donaciones/completar_donacion_manual.html', {'form': form})

def seleccionar_tipo_donacion(request, donacion_id):
    donacion = Donacion.objects.get(id=donacion_id)
    if request.method == "POST":
        tipo_donacion = request.POST.get('tipo_donacion')
        if tipo_donacion == 'dinero':
            return redirect('donaciones:donacion_dinero', donacion_id=donacion.id)
        elif tipo_donacion == 'producto':
            return redirect('donaciones:donacion_producto', donacion_id=donacion.id)
    return render(request, 'donaciones/seleccionar_tipo_donacion.html', {'donacion': donacion})

def donacion_dinero(request, donacion_id):
    donacion = Donacion.objects.get(id=donacion_id)
    if request.method == "POST":
        form = DonacionDineroForm(request.POST)
        if form.is_valid():
            donacion_dinero = form.save(commit=False)
            donacion_dinero.donacionId = donacion
            donacion_dinero.save()
            return redirect('donaciones:ingresar_dni')
    else:
        form = DonacionDineroForm()
    return render(request, 'donaciones/donacion_dinero.html', {'form': form, 'donacion': donacion})

def donacion_producto(request, donacion_id):
    donacion = Donacion.objects.get(id=donacion_id)
    if request.method == "POST":
        form = DonacionProductoForm(request.POST)
        if form.is_valid():
            donacion_producto = form.save(commit=False)
            donacion_producto.donacionId = donacion
            donacion_producto.save()
            return redirect('donaciones:ingresar_dni')
    else:
        form = DonacionProductoForm()
    return render(request, 'donaciones/donacion_producto.html', {'form': form, 'donacion': donacion})

def mercadopago(request, user_id):
    if request.method == "POST":
        form = MercadoPagoForm(request.POST)
        if form.is_valid():
            donation_amount = form.cleaned_data["monto"]

            preference = create_preference(donation_amount, user_id)

            if preference:
                return redirect(preference["response"]["init_point"])
            else:
                return render(
                    request,
                    "donaciones/mercadopago_error.html",
                    {
                        "error": "No se pudo conectar con MercadoPago. Inténtelo de nuevo más tarde."
                    },
                )
    else:
        form = MercadoPagoForm()
    return render(request, "donaciones/mercadopago.html", {"form": form})

def mercadopago_exito(request, user_id):
    payment_id = request.GET.get("payment_id")
    if payment_id:
        payment = mp.payment().get(payment_id)
        if payment["response"]["status"] == "approved":
            usuario = Usuario.objects.get(id=user_id)
            donacion = Donacion.objects.create(usuarioId=usuario)
            donation_amount = payment["response"]["transaction_amount"]
            Donacion_din.objects.create(forma_pago="mercadopago",monto=donation_amount, donacionId=donacion)
            return render(request, "donaciones/mercadopago_exito.html")
    return redirect("donaciones:mercadopago_rechazo")

def mercadopago_rechazo(request):
    return render(request, "donaciones/mercadopago_rechazo.html")


def mercadopago_pendiente(request):
    return render(request, "donaciones/mercadopago_pendiente.html")