from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from intercambios.models import Intercambio
from ofrecimientos.models import Ofrecimiento
from datetime import datetime

from django.utils import timezone
# Create your views here.

def list_exchanges_today(request):
    hoy = timezone.now().date()
    intercambios_hoy = Intercambio.objects.filter(ofrecimientoId__fecha__date=hoy)
    print(hoy)
    i = Intercambio.objects.get(id=1)
    print(i.ofrecimientoId.fecha.date())
    print(intercambios_hoy)
    return render(request, "intercambios/intercambios_del_dia.html", {"intercambios_hoy": intercambios_hoy})
