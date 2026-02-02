from django.contrib import admin
from .models import (
    ConfiguracionPagina, DatosPersonales, ExperienciaLaboral, 
    EstudioRealizado, ProductoAcademico, CategoriaTag, 
    CursoCapacitacion, Reconocimiento, VentaGarage, Idioma
)

# --- GESTIÓN DE IDIOMAS (Inline) ---
class IdiomaInline(admin.TabularInline):
    model = Idioma
    extra = 1

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'email', 'mostrar_seccion')
    list_editable = ('mostrar_seccion',)
    inlines = [IdiomaInline]
    fieldsets = (
        ('Identidad Básica', {
            'fields': (('cedula', 'sexo'), ('nombres', 'apellidos'), ('estado_civil', 'nacionalidad'), 'lugar_nacimiento', 'fecha_nacimiento', 'foto')
        }),
        ('Contacto y Ubicación', {
            'fields': (('telefono', 'telefono_convencional'), 'email', 'sitio_web', 'direccion', 'direccion_trabajo', 'licencia')
        }),
        ('Perfil y Redes Sociales', {
            'fields': ('descripcion_perfil', 'intereses', 'valores_profesionales', ('url_linkedin', 'url_github'), ('url_instagram', 'url_youtube', 'url_tiktok'), 'mostrar_seccion')
        }),
    )

@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel', 'perfil')
    list_filter = ('nombre', 'nivel')
    search_fields = ('nombre', 'perfil__nombres', 'perfil__apellidos')

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'modalidad', 'fecha_inicio', 'activo')
    list_editable = ('activo', 'modalidad')
    list_filter = ('modalidad', 'activo', 'empresa')
    search_fields = ('cargo', 'empresa', 'descripcion', 'nombre_contacto')
    
    # AGREGADO: Sección de Referencias en el formulario
    fieldsets = (
        ('Información del Puesto', {
            'fields': (('cargo', 'empresa'), 'modalidad', 'descripcion')
        }),
        ('Periodo y Estado', {
            'fields': (('fecha_inicio', 'fecha_fin'), 'activo')
        }),
        ('Referencias y Verificación', {
            'fields': (('nombre_contacto', 'telefono_contacto'),)
        }),
    )

@admin.register(EstudioRealizado)
class EstudioRealizadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'fecha_fin', 'activo')
    list_editable = ('activo',)
    list_filter = ('activo',)

@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'registro_id', 'fecha_publicacion', 'activo')
    list_filter = ('categorias', 'activo')
    filter_horizontal = ('categorias',)
    list_editable = ('activo',)
    search_fields = ('nombre', 'descripcion')

@admin.register(CategoriaTag)
class CategoriaTagAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(CursoCapacitacion)
class CursoCapacitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'institucion', 'fecha_realizacion', 'activo')
    list_editable = ('activo',)

@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'institucion', 'fecha_obtencion', 'activo')
    list_editable = ('activo',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio', 'estado', 'stock', 'activo')
    list_filter = ('estado', 'activo')
    list_editable = ('activo', 'stock')
    search_fields = ('nombre_producto',)

@admin.register(ConfiguracionPagina)
class ConfiguracionPaginaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mostrar_inicio', 'mostrar_perfil', 'mostrar_experiencia', 'mostrar_educacion', 'mostrar_contacto')
    def has_add_permission(self, request):
        return not ConfiguracionPagina.objects.exists()