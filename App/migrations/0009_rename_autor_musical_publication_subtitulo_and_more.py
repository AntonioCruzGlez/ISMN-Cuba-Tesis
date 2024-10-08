# Generated by Django 5.0.4 on 2024-06-09 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_remove_musical_publication_subtitulo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='musical_publication',
            old_name='autor',
            new_name='subtitulo',
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Medio', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior'), ('P-Media', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Atendido', 'Atendido'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('Solicitud-Inscripción', 'Solicitud-Inscripción'), ('Solicitud-ISMN', 'Solicitud-ISMN')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('RU', 'Ruso'), ('PO', 'Portugués'), ('AL', 'Alemán'), ('ES', 'Español'), ('EN', 'Inglés'), ('IT', 'Italiano'), ('FR', 'Francés')], max_length=50),
        ),
    ]
