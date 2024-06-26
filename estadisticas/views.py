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

        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

def grafico_torta(intercambios_estado):
    data = list(intercambios_estado.values())
    labels = list(intercambios_estado.keys())

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        data, labels=labels, autopct="%1.1f%%", startangle=140
    )
    #adjust_text(texts + autotexts, arrowprops=dict(arrowstyle="->", color="r", lw=1))
    ax.axis("equal")
    plt.tight_layout()

    return plt

def listar_estadisticas(request):
    return render(request, "estadisticas/listar_estadisticas.html")

def estadisticas_publicaciones(request):
    return render(request, "estadisticas/estadisticas_publicaciones.html", {
        "todas": publicaciones_estado(),
        "activas": publicaciones_activas(),
        "eliminadas": publicaciones_eliminadas(),
        "finalizadas": publicaciones_finalizadas()
    })

def publicaciones_estado():
    try:
        publicaciones = Publicacion.objects.all().exclude(estado="aceptada")
        data = [
            {
            "estado":(
                pub.estado
            )
            }
            for pub in publicaciones
        ]
        df = pd.DataFrame(data)
        values = df['estado'].value_counts(dropna=False).keys().tolist()
        counts = df['estado'].value_counts(dropna=False).tolist()
        value_dict = dict(zip(values, counts))
        img = grafico_torta(value_dict)

    except Exception:
        img = no_data()

    return create_base64_image(img)

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

def estadisticas_intercambios(request):
    return render(request, "estadisticas/estadisticas_intercambios.html", {
        "confirmadas_canceladas": intercambios_confirmados_rechazados(),
        "pendientes_finalizados": intercambios_pendientes_finalizados(),
        "pendientes_sucursal": intercambios_pendientes_sucursal(),
        "terminados_sucursal": intercambios_finalizados_sucursal(),
    })

def intercambios_confirmados_rechazados():
    try:
        intercambios = Intercambio.objects.all().exclude(estado="pendiente")
        data = [
            {
            "estado":(
                inter.estado
            )
            }
            for inter in intercambios
        ]
        df = pd.DataFrame(data)
        values = df['estado'].value_counts(dropna=False).keys().tolist()
        counts = df['estado'].value_counts(dropna=False).tolist()
        value_dict = dict(zip(values, counts))

        img = grafico_torta(value_dict)

    except Exception:
        img = no_data()
    
    return create_base64_image(img)

def intercambios_pendientes_finalizados():
    try:
        intercambios = Intercambio.objects.all()
        data = [ 
            {
            "category": (
                inter.estado if inter.estado=="pendiente" else "finalizado"
            )
            }
            for inter in intercambios
        ]

        img = grafico_barras(data)

    except Exception:
        img = no_data()
    
    return create_base64_image(img)

def intercambios_pendientes_sucursal():
    try:
        intercambios = Intercambio.objects.filter(estado="pendiente")
        data = [ 
            {
            "category": (
                inter.ofrecimientoId.sucursalId.nombre
            )
            }
            for inter in intercambios
        ]

        img = grafico_barras(data)

    except Exception:
        img = no_data()
    
    return create_base64_image(img)

def intercambios_finalizados_sucursal():
    try:
        intercambios = Intercambio.objects.all().exclude(estado="pendiente")
        data = [
            {
            "sucursal":(
                inter.ofrecimientoId.sucursalId.nombre
            )
            }
            for inter in intercambios
        ]
        df = pd.DataFrame(data)
        values = df['sucursal'].value_counts(dropna=False).keys().tolist()
        counts = df['sucursal'].value_counts(dropna=False).tolist()
        value_dict = dict(zip(values, counts))
        img = grafico_torta(value_dict)

    except Exception:
        img = no_data()
    
    return create_base64_image(img)