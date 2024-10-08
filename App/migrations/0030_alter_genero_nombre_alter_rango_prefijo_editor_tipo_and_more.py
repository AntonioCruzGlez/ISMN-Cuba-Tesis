# Generated by Django 4.2 on 2024-08-13 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0029_alter_rango_prefijo_editor_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genero',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Medio', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Media', 'P-Medio'), ('P-Inferior', 'P-Inferior'), ('P-Media_Inferior', 'P-Medio_Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('Solicitud-ISMN', 'Solicitud-ISMN'), ('Solicitud-Inscripcion', 'Solicitud-Inscripcion')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('ES', 'Español'), ('AL', 'Alemán'), ('FR', 'Francés'), ('IT', 'Italiano'), ('RU', 'Ruso'), ('PO', 'Portugués'), ('EN', 'Inglés')], max_length=50),
        ),
    ]
