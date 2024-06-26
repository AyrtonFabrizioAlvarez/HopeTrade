from django.shortcuts import render
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import io
import base64
import pandas as pd
from publicaciones.models import Publicacion
from intercambios.models import Intercambio

def create_base64_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return image_base64

def no_data():
    # Si no hay datos, mostrar un gráfico con una leyenda específica
    fig, ax = plt.subplots()
    ax.text(
        0.5,
        0.5,
        "No hay datos disponibles",
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
        fontsize=12,
    )
    plt.axis("off")
    return fig

def grafico_barras(data):
        df = pd.DataFrame(data)

        category_counts = df["category"].value_counts()

        # Crear una lista de colores
        colors = list(mcolors.TABLEAU_COLORS.values())

        # Asegurarse de que haya suficientes colores para todas las categorías
        if len(category_counts) > len(colors):
            colors = colors * (len(category_counts) // len(colors) + 1)

        plt.figure(figsize=(10, 6))
        plt.bar(
            category_counts.index,
            category_counts.values,
            color=colors[: len(category_counts)],
        )

        plt.ylabel("Número de publicaciones")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

def listar_estadisticas(request):
    return render(request, "estadisticas/listar_estadisticas.html")

def estadisticas_publicaciones(request):
    return render(request, "estadisticas/estadisticas_publicaciones.html", {
        "activas": publicaciones_activas(),
        "eliminadas": publicaciones_eliminadas(),
        "finalizadas": publicaciones_finalizadas()
    })

def publicaciones_activas():
    try:
        publicaciones = Publicacion.objects.filter(estado="disponible")
        data = [
            {
                "category": (
                    pub.categoriaId.titulo
                )
            }
            for pub in publicaciones
        ]
        img = grafico_barras(data)

    except Exception:
        img = no_data()

    return create_base64_image(img)

def publicaciones_eliminadas():
    try:
        publicaciones = Publicacion.objects.filter(estado="eliminada")
        data = [
            {
                "category": (
                    pub.categoriaId.titulo
                )
            }
            for pub in publicaciones
        ]

        img = grafico_barras(data)

    except Exception:
        img = no_data()
    
    return create_base64_image(img)

def publicaciones_finalizadas():
    try:
        publicaciones = Publicacion.objects.filter(estado="finalizada")
        data = [
            {
                "category": (
                    pub.categoriaId.titulo
                )
            }
            for pub in publicaciones
        ]

        img = grafico_barras(data)

    except Exception:
        img = no_data()

    return create_base64_image(img)

#def intercambios_estado(request):
#    try:
#        intercambios = Intercambio.objects.all()
#        data = [
#            {
#                "state": (
#                    inter.estado
#                )
#            }
#            for inter in intercambios
#        ]
#
#        return render_chart(request, "estadisticas/publicaciones_activas.html", grafico_barras(request, data))
#
#    except Exception:
#        return render_chart(request, "estadisticas/publicaciones_activas.html", no_data())