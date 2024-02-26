# Generated by Django 4.2.5 on 2024-02-06 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_alter_editor_type_alter_rango_prefijo_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prefijoeditor',
            options={'verbose_name_plural': 'Editores Prefijos'},
        ),
        migrations.AlterModelOptions(
            name='prefijopublicacion',
            options={'verbose_name_plural': 'Publicaciones Prefijos'},
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('PEND', 'Pendiente'), ('ATEND', 'Atendido')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('EADDS', 'Solicitud-Inscripción'), ('ISMNADDS', 'Solicitud-ISMN')], max_length=50),
        ),
    ]