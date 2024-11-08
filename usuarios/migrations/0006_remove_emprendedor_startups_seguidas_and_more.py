# Generated by Django 5.1 on 2024-08-20 22:08

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0001_initial'),
        ('usuarios', '0005_mentor_precio_por_hora_mentor_programa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprendedor',
            name='startups_seguidas',
        ),
        migrations.AlterField(
            model_name='emprendedor',
            name='startup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='programa_startup.startup'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='programa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='programa_startup.programa'),
        ),
        migrations.CreateModel(
            name='Mentoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('temas', models.TextField()),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada')], max_length=20)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.mentor')),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programa_startup.programa')),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programa_startup.startup')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Tarea', 'Tarea'), ('Equipo', 'Equipo'), ('Asesoria', 'Asesoria'), ('Evento', 'Evento'), ('Mentoria', 'Mentoria')], max_length=50)),
                ('mensaje', models.TextField()),
                ('leido', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SeguidorStartup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_seguimiento', models.DateTimeField(default=django.utils.timezone.now)),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguidores_startup', to='programa_startup.startup')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startups_seguidas', to='usuarios.emprendedor')),
            ],
            options={
                'verbose_name': 'Seguidor-Startup',
                'verbose_name_plural': 'Seguidores-Startups',
                'constraints': [models.UniqueConstraint(fields=('usuario', 'startup'), name='unique_seguidor_startup')],
            },
        ),
    ]
