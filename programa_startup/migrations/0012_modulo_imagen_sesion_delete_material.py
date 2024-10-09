# Generated by Django 5.1 on 2024-08-25 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0011_delete_programa'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='modulos/'),
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('video', 'Video'), ('lectura', 'Lectura'), ('ejercicio', 'Ejercicio'), ('material', 'Material Adicional')], max_length=50)),
                ('orden', models.PositiveIntegerField()),
                ('archivo', models.FileField(blank=True, null=True, upload_to='sesiones/')),
                ('url_externa', models.URLField(blank=True, max_length=255, null=True)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sesiones', to='programa_startup.sprint')),
            ],
            options={
                'verbose_name': 'sesión',
                'verbose_name_plural': 'sesiones',
                'ordering': ['orden'],
            },
        ),
        migrations.DeleteModel(
            name='Material',
        ),
    ]
