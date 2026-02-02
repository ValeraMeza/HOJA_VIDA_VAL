from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('perfil/', views.perfil, name='perfil'),
    path('experiencia/', views.experiencia, name='experiencia'),
    path('educacion/', views.educacion, name='educacion'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),
    path('trabajos/', views.trabajos, name='trabajos'),
    path('venta/', views.venta, name='venta'),
    path('contacto/', views.contacto, name='contacto'),

    # 1. Ruta para VER la pantalla de configuración (los checkboxes)
    path('generar-cv/', views.configurar_cv, name='generar_cv'),

    # 2. Ruta para PROCESAR y DESCARGAR el PDF (esta faltaba)
    path('descargar-pdf/', views.generar_cv, name='descargar_pdf'),
]