from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def prueba(request, prueba):
    return HttpResponse("<h2>pagina generalh2</h2>")

def prueba2(request):
    return render(request, "index.html")