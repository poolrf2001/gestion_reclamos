# reclamos/models.py

from django.db import models
from django.utils import timezone
import pytz
import uuid

class Reclamo(models.Model):
    ESTADOS = [
        ('Iniciado', 'Iniciado'),
        ('En_proceso', 'En proceso'),
        ('Terminado', 'Terminado'),
        ('Archivado', 'Archivado'),
    ]
    
    OFICINAS = [
        ('Alcaldía', 'Alcaldía'),
        ('Almacén', 'Almacén'),
        ('Asesoría Legal', 'Asesoría Legal'),
        ('Biblioteca', 'Biblioteca'),
        ('Bienes Patrimoniales', 'Bienes Patrimoniales'),
        ('Camal / Matadero Municipal', 'Camal / Matadero Municipal'),
        ('Defensa Civil y Gestion de Riesgos', 'Defensa Civil y Gestion de Riesgos'),
        ('Demuna y Ciam', 'Demuna y Ciam'),
        ('Fiscalización Tributaria', 'Fiscalización Tributaria'),
        ('Gerencia Municipal', 'Gerencia Municipal'),
        ('Gerencia de Administracion', 'Gerencia de Administracion'),
        ('Gerencia de Administración Tributaria','Gerencia de Administración Tributaria'),
        ('Gerencia de Desarrollo Ambiental y Fiscalizacion','Gerencia de Desarrollo Ambiental y Fiscalizacion'),
        ('Gerencia de Desarrollo Económico Social','Gerencia de Desarrollo Económico Social'),
        ('Gerencia de Desarrollo Urbano y Catastro','Gerencia de Desarrollo Urbano y Catastro'),
        ('Gerencia de Imagen Institucional','Gerencia de Imagen Institucional'),
        ('Gerencia de Infraestructura','Gerencia de Infraestructura'),
        ('Gerencia de Obras','Gerencia de Obras'),
        ('Gerencia de Planeamiento y Presupuesto','Gerencia de Planeamiento y Presupuesto'),
        ('Gerencia de Transito y Transportes','Gerencia de Transito y Transportes'),
        ('Imagen Institucional','Imagen Institucional'),
        ('Licencia de Conducir','Licencia de Conducir'),
        ('Mesa de Partes','Mesa de Partes'),
        ('OMAPED','OMAPED'),
        ('Oficina de Seguridad Ciudadana','Oficina de Seguridad Ciudadana'),
        ('Organo de Control Institucional','Organo de Control Institucional'),
        ('Policía Municipal','Policía Municipal'),
        ('Procuraduría','Procuraduría'),
        ('Programa de Complementacion Alimentaria','Programa de Complementacion Alimentaria'),
        ('Registro Civil','Registro Civil'),
        ('SISFOH','SISFOH'),
        ('Secretaria General','Secretaria General'),
        ('Serenazgo Puesto Auxilio 2','Serenazgo Puesto Auxilio 2'),
        ('Serenazgo Puesto de Auxilio 1','Serenazgo Puesto de Auxilio 1'),
        ('Sub Gerencia de Comercializacion y Pymes','Sub Gerencia de Comercializacion y Pymes'),
        ('Sub Gerencia de Contabilidad','Sub Gerencia de Contabilidad'),
        ('Sub Gerencia de Desarrollo Urbano y Catastro','Sub Gerencia de Desarrollo Urbano y Catastro'),
        ('Sub Gerencia de Ejecucion Coactiva','Sub Gerencia de Ejecucion Coactiva'),
        ('Sub Gerencia de Estudios y Pre Inversion','Sub Gerencia de Estudios y Pre Inversion'),
        ('Sub Gerencia de Limpieza Publica','Sub Gerencia de Limpieza Publica'),
        ('Sub Gerencia de Modernizacion Institucional y TI','Sub Gerencia de Modernizacion Institucional y TI'),
        ('Sub Gerencia de Obras','Sub Gerencia de Obras'),
        ('Sub Gerencia de Recursos Humanos','Sub Gerencia de Recursos Humanos'),
        ('Sub Gerencia de Servicios Orientacion y Control','Sub Gerencia de Servicios Orientacion y Control'),
        ('Sub Gerencia de Tesoreria','Sub Gerencia de Tesoreria'),
        ('Turismo','Turismo'),
        # Añadir más oficinas según sea necesario
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    distrito = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    sede = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo = models.URLField(blank=True, null=True)
    consentimiento = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Iniciado')
    oficina_recepcion = models.CharField(max_length=100, default='Secretaría General')
    oficina_derivacion = models.CharField(max_length=100, choices=OFICINAS, blank=True, null=True)
    fecha_derivacion = models.DateField(blank=True, null=True)
    hora_derivacion = models.TimeField(null=True, blank=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    mensaje_personalizado = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        local_tz = pytz.timezone('America/Lima')  # Cambia esto a tu zona horaria
        now = timezone.now().astimezone(local_tz)

        if self.oficina_derivacion and not self.fecha_derivacion:
            self.fecha_derivacion = now.date()
        if self.oficina_derivacion and not self.hora_derivacion:
            self.hora_derivacion = now.time()

        super(Reclamo, self).save(*args, **kwargs)

    def __str__(self):
        return f'Reclamo {self.codigo} - {self.nombre} {self.apellidos}'
