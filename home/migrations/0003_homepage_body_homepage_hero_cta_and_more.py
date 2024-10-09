# Generated by Django 5.1 on 2024-08-08 20:20

import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_cta',
            field=models.CharField(blank=True, help_text='Texto en pantalla que incita al usuario a una llamada de acción', max_length=255, verbose_name='Hero CTA'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_cta_link',
            field=models.ForeignKey(blank=True, help_text='Selecciona una página para enlazar la llamado de acción', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Hero CTA link'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_text',
            field=models.CharField(blank=True, help_text='Escribe una introducción del sitio', max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Imagen de la página de inicio', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='carousel_images', to='home.homepage')),
            ],
        ),
    ]
