# Generated by Django 4.2.5 on 2024-04-23 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_solicitud_deleted_alter_editor_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior'), ('P-Superior', 'P-Superior'), ('P-Medio', 'P-Medio'), ('P-Menor', 'P-Menor')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Inferior', 'P-Inferior'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Superior', 'P-Superior'), ('P-Menor', 'P-Menor'), ('P-Media', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Atendido', 'Atendido'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('Solicitud-ISMN', 'Solicitud-ISMN'), ('Solicitud-Inscripción', 'Solicitud-Inscripción')], max_length=50),
        ),
    ]
