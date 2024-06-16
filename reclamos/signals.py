# reclamos/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Reclamo
from emails.utils import send_reclamo_created_email
import uuid

@receiver(pre_save, sender=Reclamo)
def generar_codigo_antes_de_guardar(sender, instance, **kwargs):
    if not instance.codigo:
        instance.codigo = str(uuid.uuid4()).split('-')[0]

@receiver(post_save, sender=Reclamo)
def enviar_correo_creacion_reclamo(sender, instance, created, **kwargs):
    if created:
        send_reclamo_created_email(instance)
