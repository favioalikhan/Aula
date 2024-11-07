# Generated by Django 5.1 on 2024-08-21 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0006_remove_programapage_duracion_and_more'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='cronogramaitem',
            name='imagen',
            field=models.ForeignKey(blank=True, help_text='Imagen del proceso', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
