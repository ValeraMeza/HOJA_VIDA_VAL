from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

# --- VALIDADORES ---

def validar_no_futuro(value):
    """Evita que se ingresen fechas posteriores a hoy."""
    if value > date.today():
        raise ValidationError('La fecha no puede estar en el futuro.')

def validar_fecha_nacimiento(value):
    """Valida que el año de nacimiento sea lógico (1900-Hoy)."""
    if value.year < 1900:
        raise ValidationError('Por favor, ingresa un año posterior a 1900.')
    if value > date.today():
        raise ValidationError('La fecha de nacimiento no puede ser futura.')

# --- MODELOS DE APOYO ---

class CategoriaTag(models.Model):
    """Sistema de etiquetas para clasificar productos académicos."""
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Etiqueta de Clasificación"
        verbose_name_plural = "Etiquetas de Clasificación"

    def __str__(self):
        return self.nombre

# --- MODELOS PRINCIPALES ---

class DatosPersonales(models.Model):
    """Información de identidad, contacto, intereses y redes sociales del perfil."""
    SEXO_CHOICES = [('Mujer', 'Mujer'), ('Hombre', 'Hombre'), ('Otro', 'Otro')]
    ESTADO_CIVIL_CHOICES = [
        ('Soltera/o', 'Soltera/o'), ('Casada/o', 'Casada/o'),
        ('Divorciada/o', 'Divorciada/o'), ('Viuda/o', 'Viuda/o'),
        ('Unión Libre', 'Unión Libre'),
    ]

    # Identidad Básica
    cedula = models.CharField(max_length=13, verbose_name="Cédula / ID")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, verbose_name="Sexo / Género")
    estado_civil = models.CharField(max_length=30, choices=ESTADO_CIVIL_CHOICES)
    nacionalidad = models.CharField(max_length=50, default="Ecuatoriana")
    lugar_nacimiento = models.CharField(max_length=100, default="No especificado", verbose_name="Origen")
    fecha_nacimiento = models.DateField(null=True, blank=True, validators=[validar_fecha_nacimiento])
    
    # Contacto y Localización
    telefono = models.CharField(max_length=15, verbose_name="Teléfono Celular")
    telefono_convencional = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name="Correo Electrónico")
    sitio_web = models.URLField(null=True, blank=True)
    direccion = models.TextField(verbose_name="Dirección Domiciliaria")
    direccion_trabajo = models.TextField(null=True, blank=True, verbose_name="Dirección de Trabajo")
    licencia = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tipo de Licencia")
    
    # Imagen, Bio e Intereses
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)
    descripcion_perfil = models.TextField(null=True, blank=True, verbose_name="Bio (Resumen)")
    intereses = models.TextField(null=True, blank=True, help_text="Ej: Desarrollo web, diseño de interfaces, etc.")
    valores_profesionales = models.CharField(max_length=255, null=True, blank=True, help_text="Valores separados por comas")
    
    # Redes Sociales
    url_linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn URL")
    url_github = models.URLField(blank=True, null=True, verbose_name="GitHub URL")
    url_instagram = models.URLField(blank=True, null=True, verbose_name="Instagram URL")
    url_youtube = models.URLField(blank=True, null=True, verbose_name="YouTube URL")
    url_tiktok = models.URLField(blank=True, null=True, verbose_name="TikTok URL")

    mostrar_seccion = models.BooleanField(default=True, verbose_name="Sección Activa")

    class Meta:
        verbose_name = "1. Información de Identidad"
        verbose_name_plural = "1. Información de Identidad"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Idioma(models.Model):
    """Idiomas manejados por el perfil con selección predefinida."""
    IDIOMA_CHOICES = [
        ('Español', 'Español'),
        ('Inglés', 'Inglés'),
        ('Francés', 'Francés'),
        ('Alemán', 'Alemán'),
        ('Italiano', 'Italiano'),
        ('Portugués', 'Portugués'),
        ('Chino', 'Chino'),
        ('Japonés', 'Japonés'),
        ('Ruso', 'Ruso'),
        ('Otro', 'Otro'),
    ]
    
    NIVEL_CHOICES = [
        ('A1', 'A1 - Principiante'),
        ('A2', 'A2 - Elemental'),
        ('B1', 'B1 - Intermedio'),
        ('B2', 'B2 - Intermedio Alto'),
        ('C1', 'C1 - Avanzado'),
        ('C2', 'C2 - Maestría'),
        ('Nativo', 'Nativo'),
    ]
    
    nombre = models.CharField(max_length=50, choices=IDIOMA_CHOICES, verbose_name="Idioma")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nivel de Dominio")
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name="idiomas")

    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return f"{self.nombre} - {self.nivel}"
    
class ExperienciaLaboral(models.Model):
    """Registro de trayectoria profesional con modalidad de trabajo."""
    class Modalidad(models.TextChoices):
        PRESENCIAL = 'PRE', 'Presencial'
        REMOTO = 'REM', 'Remoto'
        HIBRIDO = 'HIB', 'Híbrido / Mixto'

    cargo = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150)
    fecha_inicio = models.DateField(validators=[validar_no_futuro])
    fecha_fin = models.DateField(null=True, blank=True, help_text="Vacío si es Actual", validators=[validar_no_futuro])
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    modalidad = models.CharField(
        max_length=3,
        choices=Modalidad.choices,
        default=Modalidad.PRESENCIAL,
        verbose_name="Modalidad de trabajo",
        help_text="Selecciona si el trabajo fue presencial, remoto o mixto."
    )
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono Empresa/Jefe")
    nombre_contacto = models.CharField(max_length=100, null=True, blank=True, verbose_name="Persona de Referencia")
    
    class Meta:
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "2. Trayectoria Profesional"
        # CORRECCIÓN: Quitamos el '-' para orden Ascendente (Antiguos primero)
        ordering = ['fecha_inicio'] 

    def clean(self):
        if self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError({'fecha_fin': 'La fecha de fin no puede ser anterior a la de inicio.'})

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"

class EstudioRealizado(models.Model):
    """Títulos y grados académicos obtenidos."""
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha_inicio = models.DateField(validators=[validar_no_futuro])
    fecha_fin = models.DateField(validators=[validar_no_futuro])
    certificado_pdf = models.FileField(upload_to='educacion/', null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Título Académico"
        verbose_name_plural = "3. Formación Académica"
        # CORRECCIÓN: Orden ascendente por fecha de graduación
        ordering = ['fecha_fin']

    def clean(self):
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError({'fecha_fin': 'La fecha de graduación no puede ser anterior al inicio.'})

    def __str__(self):
        return self.titulo

class ProductoAcademico(models.Model):
    """Publicaciones, proyectos o registros de propiedad intelectual."""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción Detallada")
    registro_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="ID / Registro de Propiedad")
    fecha_publicacion = models.DateField(validators=[validar_no_futuro], verbose_name="Fecha de Publicación")
    archivo = models.FileField(upload_to='academicos/', null=True, blank=True, verbose_name="Documentación (PDF/Zip)")
    categorias = models.ManyToManyField(CategoriaTag, blank=True, verbose_name="Clasificación (Tags)")
    activo = models.BooleanField(default=True, verbose_name="Visible en la web")

    @property
    def tags(self):
        return self.categorias.all().values_list('nombre', flat=True)

    class Meta:
        verbose_name = "Producto Académico"
        verbose_name_plural = "4. Producción Intelectual"
        # CORRECCIÓN: Orden ascendente por fecha publicación
        ordering = ['fecha_publicacion']

    def __str__(self):
        return f"{self.nombre} ({self.registro_id or 'S/N'})"
    
class CursoCapacitacion(models.Model):
    """Cursos de corta duración y talleres realizados."""
    nombre_curso = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha_realizacion = models.DateField(validators=[validar_no_futuro], null=True)
    horas = models.PositiveIntegerField()
    certificado_pdf = models.FileField(upload_to='cursos/', null=True, blank=True, verbose_name="Certificado (PDF)")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "5. Cursos y Certificaciones"
        # CORRECCIÓN: Orden ascendente por fecha realización
        ordering = ['fecha_realizacion']

    def __str__(self):
        return self.nombre_curso

class Reconocimiento(models.Model):
    """Premios, becas o menciones honoríficas."""
    nombre = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha_obtencion = models.DateField(validators=[validar_no_futuro], null=True)
    codigo_registro = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "6. Reconocimientos y Premios"
        # CORRECCIÓN: Orden ascendente
        ordering = ['fecha_obtencion']

    def __str__(self):
        return self.nombre

class VentaGarage(models.Model):
    """Artículos disponibles para la venta en la sección de garage."""
    ESTADO_CHOICES = [
        ('Nuevo', 'Nuevo'),
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    nombre_producto = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    imagen = models.ImageField(upload_to='venta/', null=True, blank=True)
    fecha_publicacion = models.DateField(default=timezone.now, validators=[validar_no_futuro])
    stock = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "7. Venta de Garage"
        # CORRECCIÓN: Orden ascendente (lo publicado primero sale primero)
        ordering = ['fecha_publicacion']

    def __str__(self):
        return self.nombre_producto

class ConfiguracionPagina(models.Model):
    """Ajustes globales para ocultar o mostrar secciones en la página web."""
    mostrar_inicio = models.BooleanField(default=True, verbose_name="Mostrar Inicio")
    mostrar_perfil = models.BooleanField(default=True, verbose_name="Mostrar Perfil (Datos Personales)")
    mostrar_experiencia = models.BooleanField(default=True, verbose_name="Mostrar Experiencia")
    mostrar_educacion = models.BooleanField(default=True, verbose_name="Mostrar Educación")
    mostrar_cursos = models.BooleanField(default=True, verbose_name="Mostrar Cursos")
    mostrar_logros = models.BooleanField(default=True, verbose_name="Mostrar Logros/Reconocimientos")
    mostrar_trabajos = models.BooleanField(default=True, verbose_name="Mostrar Trabajos")
    mostrar_venta = models.BooleanField(default=True, verbose_name="Mostrar Sección Venta")
    mostrar_contacto = models.BooleanField(default=True, verbose_name="Mostrar Contacto")

    class Meta:
        verbose_name = "Configuración de Visibilidad"
        verbose_name_plural = "Configuración de Visibilidad"

    def __str__(self):
        return "Ajustes de Visibilidad de Secciones"