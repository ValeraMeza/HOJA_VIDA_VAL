import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, EstudioRealizado, 
    CursoCapacitacion, Reconocimiento, ProductoLaboral, VentaGarage
)

def link_callback(uri, rel):
    """
    Convierte las URIs de Django (static y media) en rutas de archivos absolutas
    para que xhtml2pdf pueda encontrarlas en el sistema de archivos.
    """
    # Usar las configuraciones de MEDIA y STATIC de settings
    sUrl = settings.STATIC_URL      # /static/
    sRoot = settings.STATIC_ROOT    # ruta al directorio static
    mUrl = settings.MEDIA_URL       # /media/
    mRoot = settings.MEDIA_ROOT     # ruta al directorio media

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # Verificar que el archivo realmente existe
    if not os.path.isfile(path):
        return uri
    return path

def inicio(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/inicio.html', {'perfil': perfil})

def perfil(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/datos_personales.html', {'perfil': perfil})

def experiencia(request):
    perfil = DatosPersonales.objects.first()
    experiencias = ExperienciaLaboral.objects.all().order_by('-id')
    return render(request, 'curriculum/experiencia.html', {'perfil': perfil, 'experiencias': experiencias})

def educacion(request):
    perfil = DatosPersonales.objects.first()
    estudios = EstudioRealizado.objects.all().order_by('-id')
    return render(request, 'curriculum/educacion.html', {'perfil': perfil, 'estudios': estudios})

def cursos(request):
    perfil = DatosPersonales.objects.first()
    cursos = CursoCapacitacion.objects.all().order_by('-id')
    return render(request, 'curriculum/cursos.html', {'perfil': perfil, 'cursos': cursos})

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    reconocimientos = Reconocimiento.objects.all().order_by('-fecha')
    return render(request, 'curriculum/reconocimientos.html', {'perfil': perfil, 'reconocimientos': reconocimientos})

def trabajos(request):
    perfil = DatosPersonales.objects.first()
    proyectos = ProductoLaboral.objects.all().order_by('-id')
    return render(request, 'curriculum/proyectos.html', {'perfil': perfil, 'proyectos': proyectos})

def venta(request):
    perfil = DatosPersonales.objects.first()
    # Debe llamarse 'productos' para coincidir con el Canvas
    productos = VentaGarage.objects.all().order_by('-id') 
    return render(request, 'curriculum/venta.html', {
        'perfil': perfil,
        'productos': productos
    })

def contacto(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/contacto.html', {'perfil': perfil})

def generar_cv(request):
    """
    Función para generar el PDF dinámico.
    Recopila toda la información ingresada en el Admin y maneja rutas de archivos.
    """
    perfil = DatosPersonales.objects.first()
    context = {
        'perfil': perfil,
        'experiencias': ExperienciaLaboral.objects.all().order_by('-id'),
        'estudios': EstudioRealizado.objects.all().order_by('-id'),
        'cursos': CursoCapacitacion.objects.all().order_by('-id'),
        'reconocimientos': Reconocimiento.objects.all().order_by('-fecha'),
        'proyectos': ProductoLaboral.objects.all().order_by('-id'),
        'MEDIA_URL': settings.MEDIA_URL,
    }
    
    # Cargar plantilla
    template = get_template('curriculum/cv_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Hoja_de_Vida_Valeria_Meza.pdf"'

    # Creamos el PDF pasando el link_callback para resolver rutas de imágenes
    pisa_status = pisa.CreatePDF(
        html, 
        dest=response, 
        link_callback=link_callback
    )
    
    if pisa_status.err:
        return HttpResponse('Hubo un error al procesar los datos para el PDF.', status=500)
    
    return response