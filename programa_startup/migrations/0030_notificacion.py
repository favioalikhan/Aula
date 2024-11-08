# Generated by Django 5.1 on 2024-09-14 21:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0029_remove_sesion_completada_remove_tarea_entregado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Tarea', 'Tarea'), ('Equipo', 'Equipo'), ('Evento', 'Evento'), ('Mentoria', 'Mentoria')], max_length=50)),
                ('mensaje', models.TextField()),
                ('leido', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
