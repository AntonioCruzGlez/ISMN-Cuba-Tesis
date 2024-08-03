# Generated by Django 5.0.4 on 2024-08-03 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_alter_editor_ci_alter_editor_id_tribute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='CI',
            field=models.PositiveBigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='editor',
            name='id_tribute',
            field=models.PositiveBigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='editorial',
            name='id_tribute',
            field=models.PositiveBigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='CI',
            field=models.PositiveBigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio', 'P-Medio'), ('P-Inferior', 'P-Inferior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Superior', 'P-Superior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior'), ('P-Media', 'P-Medio'), ('P-Superior', 'P-Superior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='registered_data',
            name='CI',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='registered_data',
            name='id_tribute',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Atendido', 'Atendido'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('IT', 'Italiano'), ('PO', 'Portugués'), ('FR', 'Francés'), ('AL', 'Alemán'), ('RU', 'Ruso'), ('ES', 'Español'), ('EN', 'Inglés')], max_length=50),
        ),
    ]