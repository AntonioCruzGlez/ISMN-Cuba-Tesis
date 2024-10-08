# Generated by Django 5.0.4 on 2024-08-10 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0023_alter_musical_publication_autores_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musical_publication',
            name='autores',
            field=models.ManyToManyField(to='App.autor'),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Inferior', 'P-Inferior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Superior', 'P-Superior'), ('P-Medio', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior'), ('P-Superior', 'P-Superior'), ('P-Media', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('Solicitud-Inscripcion', 'Solicitud-Inscripcion'), ('Solicitud-ISMN', 'Solicitud-ISMN')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('ES', 'Español'), ('FR', 'Francés'), ('EN', 'Inglés'), ('IT', 'Italiano'), ('PO', 'Portugués'), ('AL', 'Alemán'), ('RU', 'Ruso')], max_length=50),
        ),
    ]
