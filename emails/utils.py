# emails/utils.py

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_reclamo_created_email(reclamo):
    subject = 'Tu reclamo ha sido creado'
    html_message = render_to_string('emails/reclamo_created.html', {'codigo_reclamo': reclamo.codigo})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = reclamo.correo_electronico

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_estado_updated_email(reclamo):
    subject = 'El estado de tu reclamo ha cambiado'
    html_message = render_to_string('emails/estado_updated.html', {
        'estado_reclamo': reclamo.estado,
        'mensaje_personalizado': reclamo.mensaje_personalizado
    })
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = reclamo.correo_electronico

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
