# Generated by Django 5.1 on 2024-08-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa_startup', '0026_alter_evento_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='url_externa',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
