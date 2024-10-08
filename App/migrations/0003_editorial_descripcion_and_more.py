# Generated by Django 5.0.4 on 2024-06-04 23:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_registered_data_ci_alter_rango_prefijo_editor_tipo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorial',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Menor', 'P-Menor'), ('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Medio', 'P-Medio'), ('P-Medio_Inferior', 'P-Medio_Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Menor', 'P-Menor'), ('P-Superior', 'P-Superior'), ('P-Media', 'P-Medio'), ('P-Inferior', 'P-Inferior'), ('P-Media_Inferior', 'P-Medio_Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Atendido', 'Atendido'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('EN', 'Inglés'), ('RU', 'Ruso'), ('ES', 'Español')], max_length=50),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.municipio'),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.provincia'),
        ),
    ]
