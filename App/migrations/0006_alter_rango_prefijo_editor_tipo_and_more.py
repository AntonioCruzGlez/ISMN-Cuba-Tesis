# Generated by Django 4.2.5 on 2024-03-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_musical_publication_barcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio', 'P-Medio'), ('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Menor', 'P-Menor')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Media', 'P-Medio'), ('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Menor', 'P-Menor')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('Solicitud-Inscripción', 'Solicitud-Inscripción'), ('Solicitud-ISMN', 'Solicitud-ISMN')], max_length=50),
        ),
    ]
