# Generated by Django 5.1 on 2024-08-20 22:08

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos_programas/')),
                ('beneficios', models.TextField(blank=True, null=True)),
                ('duracion', models.CharField(blank=True, max_length=50, null=True)),
                ('requisitos', models.TextField(blank=True, null=True)),
                ('criterios_evaluacion', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'programa',
                'verbose_name_plural': 'programas',
            },
        ),
        migrations.CreateModel(
            name='IntegranteStartup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=50)),
                ('fecha_inscripcion', models.DateTimeField(default=django.utils.timezone.now)),
                ('agregado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='startups_agregados', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integrante', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario-Startup',
                'verbose_name_plural': 'Usuarios-Startups',
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('orden', models.PositiveIntegerField()),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modulos', to='programa_startup.programa')),
            ],
            options={
                'verbose_name': 'módulo',
                'verbose_name_plural': 'módulos',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('orden', models.PositiveIntegerField()),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='programa_startup.modulo')),
            ],
            options={
                'verbose_name': 'sprint',
                'verbose_name_plural': 'sprints',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='sprints/materiales/')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiales', to='programa_startup.sprint')),
            ],
            options={
                'verbose_name': 'material',
                'verbose_name_plural': 'materiales',
            },
        ),
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos_startups/')),
                ('problematica', models.TextField(blank=True)),
                ('propuesta_valor', models.TextField(blank=True)),
                ('publico_objetivo', models.TextField(blank=True)),
                ('socios_clave', models.TextField(blank=True)),
                ('canales', models.TextField(blank=True, null=True)),
                ('producto_servicio', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fundador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startup_fundador', to=settings.AUTH_USER_MODEL)),
                ('integrantes', models.ManyToManyField(related_name='startups_integrante', through='programa_startup.IntegranteStartup', to=settings.AUTH_USER_MODEL)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_startups', to='programa_startup.programa')),
            ],
            options={
                'verbose_name': 'startup',
                'verbose_name_plural': 'startups',
            },
        ),
        migrations.CreateModel(
            name='Logro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logros', to='programa_startup.startup')),
            ],
            options={
                'verbose_name': 'logro',
                'verbose_name_plural': 'logros',
            },
        ),
        migrations.AddField(
            model_name='integrantestartup',
            name='startup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startup_perteneciente', to='programa_startup.startup'),
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programa_inscripciones', to='programa_startup.programa')),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startup_inscripciones', to='programa_startup.startup')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField()),
                ('tipo', models.CharField(choices=[('Programa', 'Programa'), ('Startup', 'Startup')], max_length=50)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programa_startup.programa')),
                ('startup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='programa_startup.startup')),
            ],
        ),
        migrations.CreateModel(
            name='Entregable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='entregables/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('calificacion', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprint_entregables', to='programa_startup.sprint')),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startup_entregables', to='programa_startup.startup')),
            ],
        ),
        migrations.CreateModel(
            name='StartupPrograma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateTimeField(default=django.utils.timezone.now)),
                ('progreso', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startups_participantes', to='programa_startup.programa')),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programas_asociados', to='programa_startup.startup')),
            ],
            options={
                'verbose_name': 'Startup-Programa',
                'verbose_name_plural': 'Startups-Programas',
            },
        ),
        migrations.AddConstraint(
            model_name='integrantestartup',
            constraint=models.UniqueConstraint(fields=('usuario', 'startup'), name='unique_usuario_startup'),
        ),
        migrations.AddConstraint(
            model_name='startupprograma',
            constraint=models.UniqueConstraint(fields=('startup', 'programa'), name='unique_startup_programa'),
        ),
    ]