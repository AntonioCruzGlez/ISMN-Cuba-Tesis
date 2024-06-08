# Generated by Django 5.0.4 on 2024-06-07 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_descripcionfisica_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescripcionDigital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medio', models.CharField(blank=True, choices=[('A', 'AudioLibro'), ('CA', 'Casete-audio'), ('EB', 'E-book'), ('CD', 'CD-ROM')], max_length=50, null=True)),
                ('letra', models.FileField(blank=True, null=True, upload_to='publications/letters')),
            ],
            options={
                'verbose_name_plural': 'medios digitales',
            },
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='medio_digital',
        ),
        migrations.AlterModelOptions(
            name='descripcionfisica',
            options={'verbose_name_plural': 'descripciones'},
        ),
        migrations.RemoveField(
            model_name='descripcionfisica',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='description',
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='letra',
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='numero_paginas',
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='sustrato',
        ),
        migrations.AddField(
            model_name='descripcionfisica',
            name='numero_paginas',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='descripcionfisica',
            name='tipo',
            field=models.CharField(blank=True, choices=[('LIP', 'Libro Impreso en Papel'), ('FO', 'Folleto'), ('FA', 'Fascículo'), ('B', 'Bralie')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='descripcionfisica',
            name='tipo_encuadernacion',
            field=models.CharField(blank=True, choices=[('E', 'Espiral'), ('P', 'Plástico'), ('T', 'Tela'), ('TD', 'Tapa Dura')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='descripcionfisica',
            name='tipo_impresion',
            field=models.CharField(blank=True, choices=[('O', 'Offset'), ('D', 'Digital'), ('T', 'Tipográfica'), ('X', 'Xerográfica')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Superior', 'P-Superior'), ('P-Medio', 'P-Medio'), ('P-Inferior', 'P-Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Media', 'P-Medio'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Atendido', 'Atendido'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('ES', 'Español'), ('RU', 'Ruso'), ('EN', 'Inglés')], max_length=50),
        ),
        migrations.AddField(
            model_name='musical_publication',
            name='descripcion_digital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.descripciondigital'),
        ),
        migrations.DeleteModel(
            name='DigitalMediaType',
        ),
    ]
