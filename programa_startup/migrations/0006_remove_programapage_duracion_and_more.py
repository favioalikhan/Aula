# Generated by Django 5.1 on 2024-08-21 15:35

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0005_alter_programa_pagina_programa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programapage',
            name='duracion',
        ),
        migrations.RemoveField(
            model_name='programapage',
            name='fecha_fin',
        ),
        migrations.RemoveField(
            model_name='programapage',
            name='fecha_inicio',
        ),
        migrations.CreateModel(
            name='CronogramaPrograma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modalidad', models.CharField(choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual'), ('Híbrido', 'Híbrido')], help_text='Modalidad del programa', max_length=20)),
                ('frecuencia', models.CharField(help_text='Frecuencia de clase', max_length=255)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='cronograma', to='programa_startup.programapage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CronogramaItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proceso', models.CharField(help_text='Nombre del proceso', max_length=255)),
                ('fecha_inicio', models.DateField(help_text='Fecha de inicio del proceso')),
                ('fecha_fin', models.DateField(help_text='Fecha de finalización del proceso')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='programa_startup.cronogramaprograma')),
            ],
        ),
    ]