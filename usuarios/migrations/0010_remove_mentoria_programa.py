# Generated by Django 5.1 on 2024-08-27 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_mentor_es_speaker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentoria',
            name='programa',
        ),
    ]
