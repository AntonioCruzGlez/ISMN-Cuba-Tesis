# Generated by Django 5.0.4 on 2024-06-07 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_editor_descripcion_alter_rango_prefijo_editor_tipo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescripcionFisica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, choices=[('LIP', 'Libro Impreso en Papel'), ('FO', 'Folleto'), ('FA', 'Fascículo'), ('B', 'Bralie')], max_length=100)),
                ('descripcion', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'encuadernaciones',
            },
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='encuadernacion',
        ),
        migrations.RemoveField(
            model_name='musical_publication',
            name='autor',
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio', 'P-Medio'), ('P-Superior', 'P-Superior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Media', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Atendido', 'Atendido')], max_length=50),
        ),
        migrations.AddField(
            model_name='musical_publication',
            name='descripcion_fisica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.descripcionfisica'),
        ),
        migrations.DeleteModel(
            name='EncuadernacionType',
        ),
    ]