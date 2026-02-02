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

    # Asegurarse de que path es una cadena válida antes de verificar si es archivo
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
    experiencias = ExperienciaLaboral.objects.filter(activo=True)
    return render(request, 'curriculum/experiencia.html', {'perfil': perfil, 'experiencias': experiencias})

def educacion(request):
    perfil = DatosPersonales.objects.first()
    estudios = EstudioRealizado.objects.filter(activo=True)
    return render(request, 'curriculum/educacion.html', {'perfil': perfil, 'estudios': estudios})

def cursos(request):
    perfil = DatosPersonales.objects.first()
    cursos = CursoCapacitacion.objects.filter(activo=True)
    return render(request, 'curriculum/cursos.html', {'perfil': perfil, 'cursos': cursos})

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    reconocimientos = Reconocimiento.objects.filter(activo=True)
    return render(request, 'curriculum/reconocimientos.html', {'perfil': perfil, 'reconocimientos': reconocimientos})

def trabajos(request):
    perfil = DatosPersonales.objects.first()
    proyectos = ProductoAcademico.objects.filter(activo=True)
    return render(request, 'curriculum/proyectos.html', {'perfil': perfil, 'proyectos': proyectos})

def venta(request):
    perfil = DatosPersonales.objects.first()
    productos = VentaGarage.objects.filter(activo=True) 
    context = {
        'perfil': perfil,
        'productos': productos
    }
    return render(request, 'curriculum/venta.html', context)

def contacto(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/contacto.html', {'perfil': perfil})

def configurar_cv(request):
    """
    Vista intermedia para seleccionar qué secciones mostrar en el PDF.
    Muestra un formulario con checkboxes.
    """
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/configurar_cv.html', {'perfil': perfil})

def generar_cv(request):
    """
    Función para generar el PDF dinámico.
    Permite ocultar secciones mediante parámetros GET desde configurar_cv.
    """
    # IMPORTANTE: Usamos .first() directo para tener siempre los datos básicos del perfil
    # independientemente de si la sección está 'activa' en la web o no.
    perfil = DatosPersonales.objects.first()
    
    # Capturamos los parámetros del formulario de configuración
    ocultar_foto = request.GET.get('ocultar_foto') == 'on'
    ocultar_contacto = request.GET.get('ocultar_contacto') == 'on'
    ocultar_perfil = request.GET.get('ocultar_perfil') == 'on'
    ocultar_intereses = request.GET.get('ocultar_intereses') == 'on'
    ocultar_experiencia = request.GET.get('ocultar_experiencia') == 'on'
    ocultar_educacion = request.GET.get('ocultar_educacion') == 'on'
    ocultar_cursos = request.GET.get('ocultar_cursos') == 'on'
    ocultar_idiomas = request.GET.get('ocultar_idiomas') == 'on'
    ocultar_redes = request.GET.get('ocultar_redes') == 'on'
    ocultar_valores = request.GET.get('ocultar_valores') == 'on'
    ocultar_proyectos = request.GET.get('ocultar_proyectos') == 'on'
    ocultar_reconocimientos = request.GET.get('ocultar_reconocimientos') == 'on'

    context = {
        'perfil': perfil,
        'experiencias': ExperienciaLaboral.objects.filter(activo=True),
        'estudios': EstudioRealizado.objects.filter(activo=True),
        'cursos': CursoCapacitacion.objects.filter(activo=True),
        'reconocimientos': Reconocimiento.objects.filter(activo=True),
        'proyectos': ProductoAcademico.objects.filter(activo=True),
        'MEDIA_URL': settings.MEDIA_URL,
        
        # Enviamos las banderas de control al template
        'ocultar_foto': ocultar_foto,
        'ocultar_contacto': ocultar_contacto,
        'ocultar_perfil': ocultar_perfil,
        'ocultar_intereses': ocultar_intereses,
        'ocultar_experiencia': ocultar_experiencia,
        'ocultar_educacion': ocultar_educacion,
        'ocultar_cursos': ocultar_cursos,
        'ocultar_idiomas': ocultar_idiomas,
        'ocultar_redes': ocultar_redes,
        'ocultar_valores': ocultar_valores,
        'ocultar_proyectos': ocultar_proyectos,
        'ocultar_reconocimientos': ocultar_reconocimientos,
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