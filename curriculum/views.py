import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, EstudioRealizado, 
    CursoCapacitacion, Reconocimiento, ProductoAcademico, VentaGarage
)

def link_callback(uri, rel):
    """
    Convierte las URIs de Django (static y media) en rutas de archivos absolutas
    para que xhtml2pdf pueda encontrarlas en el sistema de archivos.
    """
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):
        return uri
    return path

def inicio(request):
    # Solo mostramos si la sección está marcada como activa
    perfil = DatosPersonales.objects.filter(mostrar_seccion=True).first()
    return render(request, 'curriculum/inicio.html', {'perfil': perfil})

def perfil(request):
    perfil = DatosPersonales.objects.filter(mostrar_seccion=True).first()
    return render(request, 'curriculum/datos_personales.html', {'perfil': perfil})

def experiencia(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos por activo y el orden ya viene del Meta del modelo (-fecha_inicio)
    experiencias = ExperienciaLaboral.objects.filter(activo=True)
    return render(request, 'curriculum/experiencia.html', {'perfil': perfil, 'experiencias': experiencias})

def educacion(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos por activo y el orden ya viene del Meta del modelo (-fecha_fin)
    estudios = EstudioRealizado.objects.filter(activo=True)
    return render(request, 'curriculum/educacion.html', {'perfil': perfil, 'estudios': estudios})

def cursos(request):
    perfil = DatosPersonales.objects.first()
    # Filtramos por activo y el orden ya viene del Meta del modelo (-fecha_realizacion)
    cursos = CursoCapacitacion.objects.filter(activo=True)
    return render(request, 'curriculum/cursos.html', {'perfil': perfil, 'cursos': cursos})

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    # Corregido el campo de ordenamiento a fecha_obtencion
    reconocimientos = Reconocimiento.objects.filter(activo=True)
    return render(request, 'curriculum/reconocimientos.html', {'perfil': perfil, 'reconocimientos': reconocimientos})

def trabajos(request):
    """Vista para Productos Académicos (Renombrado de ProductoLaboral)"""
    perfil = DatosPersonales.objects.first()
    # Cambiado a ProductoAcademico y filtrado por activo
    proyectos = ProductoAcademico.objects.filter(activo=True)
    return render(request, 'curriculum/proyectos.html', {'perfil': perfil, 'proyectos': proyectos})

def venta(request):
    # Obtenemos el perfil desde el modelo DatosPersonales
    perfil = DatosPersonales.objects.first()
    
    # Filtramos los productos que están marcados como activos
    productos = VentaGarage.objects.filter(activo=True) 
    
    # Pasamos 'productos' al contexto para que coincida con el template
    context = {
        'perfil': perfil,
        'productos': productos
    }
    
    return render(request, 'curriculum/venta.html', context)

def contacto(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/contacto.html', {'perfil': perfil})

def generar_cv(request):
    """
    Función para generar el PDF dinámico.
    Solo incluye elementos marcados como 'activo'.
    """
    perfil = DatosPersonales.objects.filter(mostrar_seccion=True).first()
    context = {
        'perfil': perfil,
        'experiencias': ExperienciaLaboral.objects.filter(activo=True),
        'estudios': EstudioRealizado.objects.filter(activo=True),
        'cursos': CursoCapacitacion.objects.filter(activo=True),
        'reconocimientos': Reconocimiento.objects.filter(activo=True),
        'proyectos': ProductoAcademico.objects.filter(activo=True),
        'MEDIA_URL': settings.MEDIA_URL,
    }
    
    template = get_template('curriculum/cv_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Hoja_de_Vida.pdf"'

    pisa_status = pisa.CreatePDF(
        html, 
        dest=response, 
        link_callback=link_callback
    )
    
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF.', status=500)
    
    return response