# Generated by Django 5.1 on 2024-08-24 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_remove_emprendedor_startups_seguidas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprendedor',
            name='cargo',
        ),
    ]
