from django.contrib import admin
from .models import (
    ConfiguracionPagina, DatosPersonales, ExperienciaLaboral, 
    EstudioRealizado, ProductoAcademico, CategoriaTag, 
    CursoCapacitacion, Reconocimiento, VentaGarage, Idioma
)

class BaseAdmin(admin.ModelAdmin):
    """
    Clase base para centralizar la inyección de estilos CSS y configuraciones comunes.
    """
    class Media:
        css = {
            'all': ('curriculum/admin_custom.css',)
        }

# --- GESTIÓN DE IDIOMAS (Como Inline dentro de Datos Personales) ---
class IdiomaInline(admin.TabularInline):
    model = Idioma
    extra = 1

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(BaseAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'email', 'mostrar_seccion')
    list_editable = ('mostrar_seccion',)
    inlines = [IdiomaInline]
    
    # Organizamos los campos por secciones para optimizar el espacio y mejorar la navegación
    fieldsets = (
        ('Identidad Básica', {
            'fields': (
                ('cedula', 'sexo'), 
                ('nombres', 'apellidos'), 
                ('estado_civil', 'nacionalidad'), 
                'lugar_nacimiento', 
                'fecha_nacimiento', 
                'foto'
            )
        }),
        ('Contacto y Ubicación', {
            'fields': (
                ('telefono', 'telefono_convencional'), 
                'email', 
                'sitio_web', 
                'direccion', 
                'direccion_trabajo', 
                'licencia'
            )
        }),
        ('Perfil y Redes Sociales', {
            'fields': (
                'intereses', 
                'valores_profesionales', 
                ('url_linkedin', 'url_github'), 
                ('url_instagram', 'url_youtube', 'url_tiktok'), 
                'mostrar_seccion'
            )
        }),
    )

@admin.register(Idioma)
class IdiomaAdmin(BaseAdmin):
    list_display = ('nombre', 'nivel', 'perfil')
    # Añadimos filtros por nombre y nivel para mejorar la tabla de idiomas
    list_filter = ('nombre', 'nivel')
    search_fields = ('nombre', 'perfil__nombres', 'perfil__apellidos')

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(BaseAdmin):
    list_display = ('cargo', 'empresa', 'fecha_inicio', 'activo')
    list_editable = ('activo',)
    list_filter = ('activo', 'empresa')
    search_fields = ('cargo', 'empresa', 'descripcion')

@admin.register(EstudioRealizado)
class EstudioRealizadoAdmin(BaseAdmin):
    list_display = ('titulo', 'institucion', 'fecha_fin', 'activo')
    list_editable = ('activo',)
    list_filter = ('activo',)

@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(BaseAdmin):
    list_display = ('nombre', 'registro_id', 'fecha_publicacion', 'activo')
    list_filter = ('categorias', 'activo')
    filter_horizontal = ('categorias',)
    list_editable = ('activo',)
    search_fields = ('nombre', 'descripcion')

@admin.register(CategoriaTag)
class CategoriaTagAdmin(BaseAdmin):
    search_fields = ('nombre',)

@admin.register(CursoCapacitacion)
class CursoCapacitacionAdmin(BaseAdmin):
    list_display = ('nombre_curso', 'institucion', 'fecha_realizacion', 'activo')
    list_editable = ('activo',)

@admin.register(Reconocimiento)
class ReconocimientoAdmin(BaseAdmin):
    list_display = ('nombre', 'institucion', 'fecha_obtencion', 'activo')
    list_editable = ('activo',)

@admin.register(VentaGarage)
class VentaGarageAdmin(BaseAdmin):
    list_display = ('nombre_producto', 'precio', 'estado', 'stock', 'activo')
    list_filter = ('estado', 'activo')
    list_editable = ('activo', 'stock')
    search_fields = ('nombre_producto',)

@admin.register(ConfiguracionPagina)
class ConfiguracionPaginaAdmin(BaseAdmin):
    list_display = (
        '__str__', 
        'mostrar_inicio', 
        'mostrar_perfil', 
        'mostrar_experiencia', 
        'mostrar_educacion',
        'mostrar_contacto'
    )
    
    def has_add_permission(self, request):
        # Evita crear más de una instancia de configuración global
        return not ConfiguracionPagina.objects.exists()