from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.middleware.csrf import get_token
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Reclamo
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def consulta_reclamo(request):
    token = get_token(request)
    request.session['_csrf_token'] = token
    
    codigo = request.GET.get('codigo')

    # Validación del servidor
    if not codigo:
        return render(request, 'reclamos/consulta_reclamo.html', {'error': 'Por favor, ingrese el código del reclamo.', 'token': token})

    reclamos = Reclamo.objects.filter(codigo=codigo)

    if not reclamos.exists():
        return render(request, 'reclamos/consulta_reclamo.html', {'error': 'No se encontraron reclamos para el código proporcionado o código incorrecto.', 'token': token})

    return render(request, 'reclamos/consulta_reclamo.html', {'reclamos': reclamos, 'token': token})
@never_cache
def exportar_pdf(request):
    codigo = request.GET.get('codigo')
    reclamos = Reclamo.objects.filter(codigo=codigo)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reclamo.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        name='Title', 
        fontSize=18, 
        leading=22, 
        alignment=0,  # Alinear a la izquierda
        fontName='Helvetica-Bold'
    )
    estilo_subtitulo = ParagraphStyle(
        name='SubTitle', 
        fontSize=14, 
        leading=16, 
        spaceAfter=14, 
        alignment=0,  # Alinear a la izquierda
        fontName='Helvetica-Bold'
    )
    estilo_normal = ParagraphStyle(
        name='BodyText',
        fontSize=12,
        leading=14,
        alignment=0,  # Alinear a la izquierda
        fontName='Helvetica'
    )

    titulo = Paragraph("Libro de Reclamaciones Virtual", estilo_titulo)
    subtitulo = Paragraph("Municipalidad Provincial de Jauja", estilo_subtitulo)
    
    elements.append(titulo)
    elements.append(subtitulo)
    elements.append(Spacer(1, 12))  # Espacio entre subtitulo y contenido
 
    if reclamos.exists():
        for reclamo in reclamos:
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
                ['Descripción', Paragraph(reclamo.descripcion, estilo_normal)],
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
    else:
        elements.append(Paragraph("No se encontraron reclamos para los criterios proporcionados.", estilo_normal))

    doc.build(elements)
    return response

@never_cache
def limpiar_sesion(request):
    request.session.flush()
    return redirect('consulta_reclamo')
