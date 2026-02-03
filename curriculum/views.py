import os
import io
import requests
from pypdf import PdfWriter, PdfReader
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, EstudioRealizado, 
    CursoCapacitacion, Reconocimiento, ProductoAcademico, VentaGarage,
    ConfiguracionPagina
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

def get_visibilidad():
    """Helper para obtener la configuración de visibilidad o un valor por defecto seguro."""
    return ConfiguracionPagina.objects.first()

def inicio(request):
    # CORRECCIÓN: Usamos .first() en lugar de filtrar por mostrar_seccion.
    # Si ocultas la sección, quieres que desaparezca el bloque de contenido, 
    # pero NO el nombre/foto del header que se usa en base.html.
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/inicio.html', {
        'perfil': perfil, 
        'secciones': get_visibilidad()
    })

def perfil(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/datos_personales.html', {
        'perfil': perfil, 
        'secciones': get_visibilidad()
    })

def experiencia(request):
    perfil = DatosPersonales.objects.first()
    experiencias = ExperienciaLaboral.objects.filter(activo=True)
    return render(request, 'curriculum/experiencia.html', {
        'perfil': perfil, 
        'experiencias': experiencias,
        'secciones': get_visibilidad()
    })

def educacion(request):
    perfil = DatosPersonales.objects.first()
    estudios = EstudioRealizado.objects.filter(activo=True)
    return render(request, 'curriculum/educacion.html', {
        'perfil': perfil, 
        'estudios': estudios,
        'secciones': get_visibilidad()
    })

def cursos(request):
    perfil = DatosPersonales.objects.first()
    cursos = CursoCapacitacion.objects.filter(activo=True)
    return render(request, 'curriculum/cursos.html', {
        'perfil': perfil, 
        'cursos': cursos,
        'secciones': get_visibilidad()
    })

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    reconocimientos = Reconocimiento.objects.filter(activo=True)
    return render(request, 'curriculum/reconocimientos.html', {
        'perfil': perfil, 
        'reconocimientos': reconocimientos,
        'secciones': get_visibilidad()
    })

def trabajos(request):
    perfil = DatosPersonales.objects.first()
    proyectos = ProductoAcademico.objects.filter(activo=True)
    return render(request, 'curriculum/proyectos.html', {
        'perfil': perfil, 
        'proyectos': proyectos,
        'secciones': get_visibilidad()
    })

def venta(request):
    perfil = DatosPersonales.objects.first()
    productos = VentaGarage.objects.filter(activo=True) 
    context = {
        'perfil': perfil,
        'productos': productos,
        'secciones': get_visibilidad()
    }
    # CORRECCIÓN: Cambiado de 'venta_garage.html' a 'venta.html' para coincidir con tu archivo
    return render(request, 'curriculum/venta.html', context)

def contacto(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/contacto.html', {
        'perfil': perfil, 
        'secciones': get_visibilidad()
    })

def configurar_cv(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/configurar_cv.html', {'perfil': perfil})

def checkout(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'curriculum/checkout.html', {
        'perfil': perfil,
        'secciones': get_visibilidad()
    })

def generar_cv(request):
    perfil = DatosPersonales.objects.first()
    
    scheme = request.scheme
    host = request.get_host()
    base_url = f"{scheme}://{host}"
    
    # Captura de parámetros (Banderas booleanas)
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
    ocultar_venta = request.GET.get('ocultar_venta') == 'on'
    ocultar_anexos = request.GET.get('ocultar_anexos') == 'on'

    # CORRECCIÓN: Definimos las variables AQUÍ para usarlas tanto en context como en el loop de anexos
    experiencias = ExperienciaLaboral.objects.filter(activo=True)
    estudios = EstudioRealizado.objects.filter(activo=True)
    proyectos = ProductoAcademico.objects.filter(activo=True)
    cursos = CursoCapacitacion.objects.filter(activo=True)
    reconocimientos = Reconocimiento.objects.filter(activo=True)
    productos_venta = VentaGarage.objects.filter(activo=True)

    context = {
        'perfil': perfil,
        'experiencias': experiencias, # Ahora usamos la variable definida arriba
        'estudios': estudios,
        'cursos': cursos,
        'reconocimientos': reconocimientos,
        'proyectos': proyectos,
        'productos': productos_venta,
        'MEDIA_URL': settings.MEDIA_URL,
        'base_url': base_url,
        
        # Banderas
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
        'ocultar_venta': ocultar_venta,
        'ocultar_anexos': ocultar_anexos,
    }
    
    template = get_template('curriculum/cv_pdf.html')
    html = template.render(context)
    
    cv_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=cv_buffer, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF principal.', status=500)

    merger = PdfWriter()
    cv_buffer.seek(0)
    merger.append(cv_buffer)

    def adjuntar_archivo(campo_archivo):
        try:
            if not campo_archivo: return
            
            content = None
            if hasattr(campo_archivo, 'url') and campo_archivo.url.startswith('http'):
                response = requests.get(campo_archivo.url)
                if response.status_code == 200:
                    content = response.content
            else:
                try:
                    with campo_archivo.open('rb') as f:
                        content = f.read()
                except Exception:
                    pass

            if content and content.startswith(b'%PDF'):
                merger.append(io.BytesIO(content))
        except Exception as e:
            print(f"Error adjuntando archivo: {e}")

    # LÓGICA DE FUSIÓN (ANEXOS)
    if not ocultar_anexos:
        # CORRECCIÓN: Usamos la variable booleana 'ocultar_experiencia' en lugar de request.GET
        # Y 'experiencias' ahora está definida correctamente.
        if not ocultar_experiencia:
            for exp in experiencias:
                adjuntar_archivo(exp.certificado_pdf)
                
        if not ocultar_educacion:
            for estudio in estudios:
                adjuntar_archivo(estudio.certificado_pdf)

        if not ocultar_proyectos:
            for proyecto in proyectos:
                adjuntar_archivo(proyecto.archivo)
                
        if not ocultar_cursos:
            for curso in cursos:
                adjuntar_archivo(curso.certificado_pdf)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Hoja_de_Vida.pdf"'
    
    merger.write(response)
    
    return response