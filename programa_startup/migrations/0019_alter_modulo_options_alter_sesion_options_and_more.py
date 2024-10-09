# Generated by Django 5.1 on 2024-08-25 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0018_sprint_sesion_entregable_tarea'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modulo',
            options={'verbose_name': 'módulo', 'verbose_name_plural': 'módulos'},
        ),
        migrations.AlterModelOptions(
            name='sesion',
            options={'verbose_name': 'sesión', 'verbose_name_plural': 'sesiones'},
        ),
        migrations.AlterModelOptions(
            name='sprint',
            options={'verbose_name': 'sprint', 'verbose_name_plural': 'sprints'},
        ),
        migrations.RemoveField(
            model_name='modulo',
            name='orden',
        ),
        migrations.RemoveField(
            model_name='sesion',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='sesion',
            name='orden',
        ),
        migrations.RemoveField(
            model_name='sprint',
            name='orden',
        ),
    ]