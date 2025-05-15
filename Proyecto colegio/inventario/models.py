from django.db import models
from django.core.files.base import ContentFile
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import random

class Inventario(models.Model):
    TIPO_EQUIPO_CHOICES = [
        ('Audio', 'Audio'),
        ('Cámara', 'Cámara'),
        ('Impresora', 'Impresora'),
        ('Notebook', 'Notebook'),
        ('Otros', 'Otros'),
        ('PC', 'PC'),
        ('Proyector', 'Proyector'),
        ('Tv', 'TV'),
    ]

    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('En mantenimiento', 'En mantenimiento'),
        ('Dañado', 'Dañado'),
        ('De baja', 'De baja'),
    ]

    UBICACION_CHOICES = [
        ('Bodega', 'Bodega'),
        ('Capellanía', 'Capellanía'),
        ('Comedor', 'Comedor'),
        ('Computación', 'Computación'),
        ('Dirección', 'Dirección'),
        ('Inspectoría', 'Inspectoría'),
        ('Integración', 'Integración'),
        ('Patio', 'Patio'),
        ('PMI', 'PMI'),
        ('Prebásica', 'Prebásica'),
        ('Sala 1', 'Sala 1'),
        ('Sala 2', 'Sala 2'),
        ('Sala 3', 'Sala 3'),
        ('Sala Profesores', 'Sala Profesores'),
        ('Sala Taller', 'Sala Taller'),
        ('Secretaría', 'Secretaría'),
        ('Templo', 'Templo'),
        ('UTP', 'UTP'),
    ]

    FONDO_ADQUISICION_CHOICES = [
        ('Sep', 'SEP'),
        ('Pie', 'PIE'),
        ('Sub Esc', 'SUB ESC'),
        ('Otro', 'OTRO')
    ]

    equipo = models.CharField(max_length=100)
    tipo_equipo = models.CharField(max_length=50, choices=TIPO_EQUIPO_CHOICES)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, choices=UBICACION_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    detalle = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=13, unique=True, editable=False)
    codigo_barras = models.ImageField(upload_to='codigos_barras/', blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_equipos/', blank=True, null=True)

    prestamo_activo = models.BooleanField(default=False)
    nombre_solicitante = models.CharField(max_length=100, blank=True, null=True)
    fecha_inicio_prestamo = models.DateField(blank=True, null=True)
    fecha_fin_prestamo = models.DateField(blank=True, null=True)

    duracion = models.IntegerField(blank=True, null=True)

    fondo_adquisicion = models.CharField(max_length=100, choices=FONDO_ADQUISICION_CHOICES, default='OTRO')
    fecha_adquisicion = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.marca = self.marca.title() if self.marca else self.marca
        self.modelo = self.modelo.title() if self.modelo else self.modelo

        # Normalizar campos para coincidir con los valores de choices
        ubic_dict = dict(self.UBICACION_CHOICES)
        estado_dict = dict(self.ESTADO_CHOICES)

        if self.ubicacion:
            for k, v in ubic_dict.items():
                if self.ubicacion.lower() == k.lower() or self.ubicacion.lower() == v.lower():
                    self.ubicacion = k
                    break

        if self.estado:
            for k, v in estado_dict.items():
                if self.estado.lower() == k.lower() or self.estado.lower() == v.lower():
                    self.estado = k
                    break

        if self.tipo_equipo and self.tipo_equipo.lower() == 'pc':
            self.tipo_equipo = 'PC'

        if not self.codigo:
            while True:
                nuevo_codigo = ''.join(str(random.randint(0, 9)) for _ in range(12))
                if not Inventario.objects.filter(codigo=nuevo_codigo).exists():
                    self.codigo = nuevo_codigo
                    break

        if self.codigo and len(self.codigo) == 12 and (not self.codigo_barras or not self.codigo_barras.name):
            EAN13 = barcode.get_barcode_class('ean13')
            barcode_obj = EAN13(self.codigo, writer=ImageWriter())
            buffer = BytesIO()

            options = {
                'module_height': 5.5,
                'font_size': 8,
                'text_distance': 5.0,
                'quiet_zone': 2.0,
                'write_text': True
            }

            barcode_obj.write(buffer, options=options)
            self.codigo_barras.save(f"{self.codigo}.png", ContentFile(buffer.getvalue()), save=False)

        if self.fecha_inicio_prestamo and self.fecha_fin_prestamo:
            self.duracion = (self.fecha_fin_prestamo - self.fecha_inicio_prestamo).days
        else:
            self.duracion = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipo} - {self.marca} {self.modelo}"
