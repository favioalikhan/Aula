# Generated by Django 5.1 on 2024-08-25 03:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0010_remove_programa_pagina_programa_and_more'),
        ('usuarios', '0007_remove_emprendedor_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='programa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='programa_startup.programapage'),
        ),
        migrations.AlterField(
            model_name='mentoria',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programa_startup.programapage'),
        ),
    ]
