# reclamos/admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from .models import Reclamo
from .resources import ReclamoResource
from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils.html import format_html
from emails.utils import send_reclamo_created_email, send_estado_updated_email 
import uuid# Importar la función de envío de correo

admin.site.site_header = "Gestión de Reclamos Admin"
admin.site.site_title = "Panel de Administración de Reclamos"
admin.site.index_title = "Bienvenido al Panel de Administración"

def exportar_pdf_admin(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reclamos.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_subtitulo = ParagraphStyle(name='SubTitle', fontSize=14, leading=16, spaceAfter=14, alignment=1)
    estilo_normal = styles['BodyText']
      # Centrar texto

    titulo = Paragraph("Libro de Reclamaciones Virtual", estilo_titulo)
    subtitulo = Paragraph("Municipalidad Provincial de Jauja", estilo_normal)
    
    elements.append(titulo)
    elements.append(subtitulo)
    elements.append(Paragraph("<br/><br/>", estilo_normal))  # Espacio entre subtitulo y contenido

    for reclamo in queryset:
        # Sección de detalles del reclamo
        elements.append(Paragraph("Detalles del Reclamo", estilo_subtitulo))
        data_reclamo = [
            ['Código del Reclamo', reclamo.codigo],
            ['Nombre', f"{reclamo.nombre} {reclamo.apellidos}"],
            ['Documento', f"{reclamo.tipo_documento} {reclamo.numero_documento}"],
            ['Correo Electrónico', reclamo.correo_electronico],
            ['Teléfono', reclamo.telefono],
            ['Dirección', reclamo.direccion],
            ['Distrito', reclamo.distrito],
            ['Provincia', reclamo.provincia],
            ['Fecha', reclamo.fecha],
            ['Hora', reclamo.hora],
            ['Sede', reclamo.sede],
            ['Descripción', Paragraph(reclamo.descripcion, styles['BodyText'])],
        ]
        table_reclamo = Table(data_reclamo, colWidths=[150, 300])
        table_reclamo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightcyan),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('BOX', (0, 0), (-1, -1), 1, colors.white),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('ROUNDED', (0, 0), (-1, -1), 1, 3),
            ('VALIGN', (0, -1), (-1, -1), 'TOP')
        ]))
        elements.append(table_reclamo)
        elements.append(Spacer(1, 12))  # Espacio entre secciones

        # Sección de detalles del estado del reclamo
        elements.append(Paragraph("Detalles del Estado del Reclamo", estilo_subtitulo))
        data_estado = [
            ['Estado', reclamo.estado],
            ['Oficina Recepción', reclamo.oficina_recepcion],
            ['Oficina Derivación', reclamo.oficina_derivacion],
            ['Fecha Derivación', reclamo.fecha_derivacion],
            ['Hora Derivación', reclamo.hora_derivacion],
        ]
        table_estado = Table(data_estado, colWidths=[150, 300])
        table_estado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightcyan),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('BOX', (0, 0), (-1, -1), 1, colors.white),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('ROUNDED', (0, 0), (-1, -1), 1, 3),
        ]))
        elements.append(table_estado)
        elements.append(Spacer(1, 24))  # Espacio entre registros si hay múltiples reclamos

    doc.build(elements)
    return response


exportar_pdf_admin.short_description = "Exportar a PDF"

def enviar_correos(modeladmin, request, queryset):
    for reclamo in queryset:
        if not reclamo.codigo:
            reclamo.codigo = str(uuid.uuid4()).split('-')[0]
            reclamo.save()
        send_reclamo_created_email(reclamo)
enviar_correos.short_description = "Enviar correos con códigos"

class ReclamoAdmin(ImportExportModelAdmin):
    resource_class = ReclamoResource
    list_display = ('codigo','nombre', 'apellidos', 'tipo_documento', 'numero_documento', 'estado_colored', 'fecha', 'sede', 'oficina_recepcion', 'oficina_derivacion', 'fecha_derivacion')
    list_filter = ('estado', 'fecha', 'sede', 'oficina_derivacion')
    search_fields = ('nombre', 'apellidos', 'numero_documento')
    actions = [exportar_pdf_admin, enviar_correos]

    readonly_fields = ('nombre', 'apellidos', 'tipo_documento', 'numero_documento', 'correo_electronico', 'telefono', 'direccion', 'distrito', 'provincia', 'fecha', 'hora', 'sede', 'descripcion', 'archivo', 'consentimiento', 'oficina_recepcion', 'codigo', 'fecha_derivacion', 'hora_derivacion')

    fieldsets = (
        (None, {
            'fields': (
                'nombre', 'apellidos', 'tipo_documento', 'numero_documento', 'correo_electronico', 'telefono', 'direccion', 
                'distrito', 'provincia', 'fecha', 'hora', 'sede', 'descripcion', 'archivo', 'consentimiento'
            )
        }),
        ('Gestión de Reclamo', {
            'fields': ('estado', 'oficina_recepcion', 'oficina_derivacion', 'fecha_derivacion', 'hora_derivacion', 'mensaje_personalizado')  # Añadir mensaje_personalizado aquí
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.oficina_derivacion:
            # Guardar la hora y fecha local
            local_time = timezone.localtime()
            if not obj.fecha_derivacion:
                obj.fecha_derivacion = local_time.date()
            if not obj.hora_derivacion:
                obj.hora_derivacion = local_time.time()
        if change:  # Si el objeto está siendo actualizado
            reclamo = Reclamo.objects.get(pk=obj.pk)
            if 'estado' in form.changed_data:  # Si el estado ha cambiado
                send_estado_updated_email(obj)  # Enviar el correo al actualizar el estado
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def estado_colored(self, obj):
        if obj.estado == 'Iniciado':
            color = 'blue'
        elif obj.estado == 'En_proceso':
            color = 'orange'
        elif obj.estado == 'Terminado':
            color = 'green'
        elif obj.estado == 'Archivado':
            color = 'red'
        else:
            color = 'black'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_estado_display())

    estado_colored.short_description = 'Estado'
    
admin.site.register(Reclamo, ReclamoAdmin)
