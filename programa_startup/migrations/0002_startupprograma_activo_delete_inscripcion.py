# Generated by Django 5.1 on 2024-08-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='startupprograma',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Inscripcion',
        ),
    ]
