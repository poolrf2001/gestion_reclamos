# Generated by Django 5.0.6 on 2024-06-11 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamos', '0002_alter_reclamo_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclamo',
            name='mensaje_personalizado',
            field=models.TextField(blank=True, null=True),
        ),
    ]
