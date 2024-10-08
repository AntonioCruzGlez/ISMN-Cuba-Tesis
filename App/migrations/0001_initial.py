# Generated by Django 5.0.4 on 2024-06-02 01:08

import App.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('nacionalidad', models.CharField(choices=[('CUB', 'Cuba'), ('ITA', 'Italia'), ('EUA', 'Estados Unidos')], max_length=50)),
                ('Rol', models.CharField(choices=[('AUT', 'Autor'), ('ADP', 'Adaptador'), ('EDM', 'Editor Musical'), ('ARR', 'Arreglista')], max_length=50)),
            ],
            options={
                'verbose_name_plural': 'autores',
            },
        ),
        migrations.CreateModel(
            name='Caracterizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_fundacion', models.DateField(validators=[App.models.validate_date])),
                ('actividad_principal', models.CharField(choices=[('E', 'Editorial'), ('EUOU', 'Editorial Universitaria o Universidad'), ('EOENE', 'Empresa o Entidad no Editorial'), ('IEDU', 'Institución Educativa diferente a Universidad'), ('IR', 'Institución Religiosa')], max_length=45)),
                ('naturaleza_juridica', models.CharField(choices=[('EM', 'Empresa Mixta'), ('A', 'Asociación'), ('ECE', 'Empresa Comercial del Estado'), ('M', 'Ministerio')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DigitalMediaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'medios digitales',
            },
        ),
        migrations.CreateModel(
            name='EncuadernacionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'encuadernaciones',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'géneros',
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'materias',
            },
        ),
        migrations.CreateModel(
            name='PrefijoEditor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(unique=True)),
                ('lote', models.CharField(max_length=7)),
            ],
            options={
                'verbose_name_plural': 'Prefijos-Editores',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rango_Prefijo_Editor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_inferior', models.PositiveIntegerField()),
                ('rango_superior', models.PositiveIntegerField()),
                ('tipo', models.CharField(choices=[('P-Inferior', 'P-Inferior'), ('P-Superior', 'P-Superior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Medio', 'P-Medio'), ('P-Menor', 'P-Menor')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Rangos-Editores',
            },
        ),
        migrations.CreateModel(
            name='Rango_Prefijo_Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_superior', models.PositiveIntegerField()),
                ('tipo', models.CharField(choices=[('P-Inferior', 'P-Inferior'), ('P-Superior', 'P-Superior'), ('P-Media', 'P-Medio'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Menor', 'P-Menor')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Rango-Publicaciones',
            },
        ),
        migrations.CreateModel(
            name='Registered_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('id_tribute', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Registrados',
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coleccion', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_coleccion', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('tipo_publicacion', models.CharField(choices=[('P', 'Partitura'), ('PO', 'Partitura de Orquesta'), ('RP', 'Reducción para Piano')], max_length=50)),
                ('idioma', models.CharField(choices=[('EN', 'Inglés'), ('RU', 'Ruso'), ('ES', 'Español')], max_length=50)),
            ],
            options={
                'verbose_name_plural': 'temas',
            },
        ),
        migrations.CreateModel(
            name='CopyDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('name_BD', models.CharField(max_length=100)),
                ('rute_BD', models.CharField(max_length=600)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=14, unique=True, validators=[App.models.validate_phone])),
                ('birthday', models.DateField(blank=True, null=True, validators=[App.models.validate_date])),
                ('image_profile', models.ImageField(blank=True, default='profile_default.png', upload_to='profile', validators=[App.models.validate_image_extension])),
                ('id_tribute', models.PositiveSmallIntegerField(unique=True)),
                ('state', models.BooleanField(default=True)),
                ('CI', models.PositiveSmallIntegerField(blank=True, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('prefijo', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='App.prefijoeditor')),
            ],
            options={
                'verbose_name_plural': 'editores',
            },
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=14, unique=True, validators=[App.models.validate_phone])),
                ('image_profile', models.ImageField(blank=True, default='profile_default.png', upload_to='profile', validators=[App.models.validate_image_extension])),
                ('id_tribute', models.PositiveSmallIntegerField(unique=True)),
                ('state', models.BooleanField(default=True)),
                ('sigla', models.CharField(blank=True, max_length=10, null=True)),
                ('nombre_sello', models.CharField(max_length=100)),
                ('nombre_responsable', models.CharField(max_length=50)),
                ('apellidos_responsable', models.CharField(max_length=50)),
                ('caracterizacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.caracterizacion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('prefijo', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='App.prefijoeditor')),
            ],
            options={
                'verbose_name_plural': 'editoriales',
            },
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=14, unique=True, validators=[App.models.validate_phone])),
                ('note', models.TextField(blank=True)),
                ('image_profile', models.ImageField(blank=True, default='profile_default.png', upload_to='profile', validators=[App.models.validate_image_extension])),
                ('directions', models.CharField(max_length=150)),
                ('CI', models.PositiveSmallIntegerField(unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'especialistas',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipios', to='App.provincia')),
            ],
        ),
        migrations.AddField(
            model_name='prefijoeditor',
            name='rango',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.rango_prefijo_editor'),
        ),
        migrations.CreateModel(
            name='PrefijoPublicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('lote', models.CharField(max_length=7)),
                ('rango', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.rango_prefijo_publicacion')),
            ],
            options={
                'verbose_name_plural': 'Publicaciones Prefijos',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temporal', models.JSONField()),
                ('tipo', models.CharField(choices=[('Solicitud-ISMN', 'Solicitud-ISMN'), ('Solicitud-Inscripción', 'Solicitud-Inscripción')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Atendido', 'Atendido'), ('Pendiente', 'Pendiente')], max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.editor')),
                ('editorial', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.editorial')),
            ],
            options={
                'verbose_name_plural': 'solicitudes',
            },
        ),
        migrations.CreateModel(
            name='Musical_Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('subtitulo', models.CharField(blank=True, max_length=50, null=True)),
                ('autor', models.CharField(max_length=100)),
                ('ismn', models.CharField(max_length=20, unique=True)),
                ('barcode', models.ImageField(upload_to='publications/barcodes')),
                ('letra', models.FileField(upload_to='publications/letters')),
                ('imagen', models.ImageField(blank=True, default='default.jpg', upload_to='publications')),
                ('date_time', models.DateTimeField(validators=[App.models.validate_date])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sustrato', models.CharField(choices=[('PI', 'Publicación Impresa'), ('PE', 'Publicacion Electrónica')], default='PI', max_length=2)),
                ('numero_paginas', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('autores', models.ManyToManyField(to='App.autor')),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.editor')),
                ('editorial', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.editorial')),
                ('encuadernacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.encuadernaciontype')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.genero')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.materia')),
                ('medio_digital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.digitalmediatype')),
                ('prefijo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.prefijopublicacion')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.tema')),
            ],
            options={
                'verbose_name_plural': 'publicaciones',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=150)),
                ('municipio', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='App.municipio')),
                ('provincia', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='App.provincia')),
            ],
            options={
                'verbose_name_plural': 'ubicaciones',
            },
        ),
        migrations.AddField(
            model_name='editorial',
            name='ubicacion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.ubicacion'),
        ),
        migrations.AddField(
            model_name='editor',
            name='ubicacion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.ubicacion'),
        ),
    ]
