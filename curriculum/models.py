from django.db import models



class DatosPersonales(models.Model):
    # Opciones para campos de selección
    SEXO_CHOICES = [
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre'),
        ('Otro', 'Otro'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('Soltera/o', 'Soltera/o'),
        ('Casada/o', 'Casada/o'),
        ('Divorciada/o', 'Divorciada/o'),
        ('Viuda/o', 'Viuda/o'),
        ('Unión Libre', 'Unión Libre'),
    ]

    # Identidad Básica
    cedula = models.CharField(max_length=13, verbose_name="Cédula / ID")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES)
    estado_civil = models.CharField(max_length=30, choices=ESTADO_CIVIL_CHOICES)
    
    # Origen y Fecha
    nacionalidad = models.CharField(max_length=50, default="Ecuatoriana")
    lugar_nacimiento = models.CharField(max_length=100, default="No especificado")
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    # Contacto
    telefono = models.CharField(max_length=15, verbose_name="Teléfono Celular")
    telefono_convencional = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name="Correo Electrónico")
    sitio_web = models.URLField(null=True, blank=True)
    
    # Ubicación y Otros
    direccion = models.TextField(verbose_name="Dirección Domiciliaria")
    direccion_trabajo = models.TextField(null=True, blank=True, verbose_name="Dirección Laboral")
    licencia = models.CharField(max_length=50, null=True, blank=True, verbose_name="Licencia de Conducir")
    
    # Multimedia y Perfil
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)
    descripcion_perfil = models.TextField(null=True, blank=True, verbose_name="Perfil Profesional (Bio)")
    
    # Redes Sociales
    url_linkedin = models.URLField(null=True, blank=True, verbose_name="URL LinkedIn")
    url_instagram = models.URLField(null=True, blank=True, verbose_name="URL Instagram")
    url_github = models.URLField(null=True, blank=True, verbose_name="URL GitHub")

    class Meta:
        verbose_name = "Datos Personales"
        verbose_name_plural = "Datos Personales"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    cargo = models.CharField(max_length=150, default="Cargo no especificado")
    empresa = models.CharField(max_length=150, default="Empresa no especificada")
    fecha_inicio = models.CharField(max_length=50, default="Fecha de inicio") 
    fecha_fin = models.CharField(max_length=50, default="Actualidad")
    descripcion = models.TextField(default="Sin descripción de funciones")
    ubicacion = models.CharField(max_length=100, default="Ubicación no especificada")

    class Meta:
        verbose_name_plural = "Experiencias Laborales"

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

class EstudioRealizado(models.Model):
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha_inicio = models.CharField(max_length=50)
    fecha_fin = models.CharField(max_length=50)
    certificado_pdf = models.FileField(
        upload_to='educacion/certificados/', 
        null=True, 
        blank=True,
        help_text="Sube aquí el diploma o certificado en formato PDF"
    )

    class Meta:
        verbose_name_plural = "Estudios Realizados"

    def __str__(self):
        return self.titulo

class CursoCapacitacion(models.Model):
    nombre_curso = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    horas = models.CharField(max_length=50)
    certificado_pdf = models.FileField(
        upload_to='cursos/certificados/', 
        null=True, 
        blank=True,
        help_text="Sube el certificado del curso en formato PDF"
    )
    class Meta:
        verbose_name_plural = "Cursos y Formaciones"

    def __str__(self):
        return self.nombre_curso

class Reconocimiento(models.Model):
    nombre = models.CharField(max_length=200, default="Reconocimiento no especificado")
    institucion = models.CharField(max_length=200, default="Institución no especificada")
    fecha = models.CharField(max_length=50, default="Fecha no especificada")
    codigo_registro = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        verbose_name_plural = "Reconocimientos y Premios"

    def __str__(self):
        return self.nombre

class ProductoLaboral(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.CharField(max_length=50)
    registro_id = models.CharField(max_length=50)
    
    # NUEVO CAMPO: Para subir archivos, portafolios o documentación técnica
    archivo = models.FileField(
        upload_to='proyectos/archivos/', 
        null=True, 
        blank=True,
        help_text="Sube aquí la documentación o el archivo del proyecto (PDF recomendado)"
    )

    class Meta:
        verbose_name_plural = "Productos Laborales"

    def __str__(self):
        return self.nombre

class VentaGarage(models.Model):
    nombre_producto = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=[('Nuevo', 'Nuevo'), ('Como Nuevo', 'Como Nuevo'), ('Usado', 'Usado')])
    item_id = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='venta/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=1, help_text="Cantidad de unidades disponibles")

    class Meta:
        verbose_name_plural = "Venta de Garage"

    def __str__(self):
        return self.nombre_producto