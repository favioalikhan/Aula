# Generated by Django 5.1 on 2024-08-26 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_alter_mentor_programa_alter_mentoria_programa'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='es_speaker',
            field=models.BooleanField(default=False),
        ),
    ]
