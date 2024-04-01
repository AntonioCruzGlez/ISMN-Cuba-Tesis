import base64
from datetime import datetime
from random import randint
from smtplib import SMTPServerDisconnected

from PIL import Image as PILImage, ImageDraw
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pathlib import Path

from App.models import (Editor, Musical_Publication, Registered_Data, PrefijoEditor, PrefijoPublicacion,
                        Rango_Prefijo_Editor, Rango_Prefijo_Publicacion, Solicitud)
from django.views.decorators.cache import cache_control
from django.contrib import messages  # Return messages
from django.http import HttpResponseRedirect, QueryDict  # Redirect the page after submit
from django.db.models import Q, Max, Count
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives  # Required to send emails
from django.template import loader  # Render templates on email body
from django.contrib.auth.views import LoginView, LogoutView
import io
from django.http import FileResponse
# REPORTLAB
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, letter

# ================= VARIABLES TEMPORALES =================
datos = QueryDict

# ================= SECCIÓN DE SEGURIDAD Y AUTENTICACIÓN =================
class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    next_page = '/'


class MyLogoutView(LogoutView):
    next_page = '/'


# ================= SECCIÓN DE CREACIÓN DE RANGOS Y PREFIJOS =================
def generate_prefijo_editor(range):
    value = 0
    lote = '979-0'
    if range == 'p-menor':
        max_menor = PrefijoEditor.objects.filter(rango__tipo='P-Menor').aggregate(Max('value'))['value__max']
        if max_menor:
            value = max_menor + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Menor'))
        else:
            return PrefijoEditor.objects.create(value=100001, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Menor'))
    elif range == 'p-inferior':
        max_inferior = PrefijoEditor.objects.filter(rango__tipo='P-Inferior').aggregate(Max('value'))['value__max']
        if max_inferior:
            value = max_inferior + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Inferior'))
        else:
            return PrefijoEditor.objects.create(value=10001, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Inferior'))
    elif range == 'p-medio_inferior':
        max_medio_inf = PrefijoEditor.objects.filter(rango__tipo='P-Medio_Inferior').aggregate(Max('value'))[
            'value__max']
        if max_medio_inf:
            value = max_medio_inf + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio_Inferior'))
        else:
            return PrefijoEditor.objects.create(value=1001, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio_Inferior'))
    elif range == 'p-medio':
        max_medio = PrefijoEditor.objects.filter(rango__tipo='P-Medio').aggregate(Max('value'))['value__max']
        if max_medio:
            value = max_medio + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio'))
        else:
            return PrefijoEditor.objects.create(value=101, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio'))
    elif range == 'p-superior':
        max_superior = PrefijoEditor.objects.filter(rango__tipo='P-Superior').aggregate(Max('value'))['value__max']
        if max_superior:
            value = max_superior + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Superior'))
        else:
            return PrefijoEditor.objects.create(value=1, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Superior'))


def generate_prefijo_publicacion(valor):
    if valor.__len__() == 2:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(tipo='P-Menor'))
        return prefijo
    elif valor.__len__() == 3:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(
                                                        tipo='P-Inferior'))
        return prefijo
    elif valor.__len__() == 4:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(
                                                        tipo='P-Media_Inferior'))
        return prefijo
    elif valor.__len__() == 5:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(tipo='P-Media'))
        return prefijo
    else:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(
                                                        tipo='P-Superior'))
        return prefijo


# Registration Function
def register_user(request):
    if request.method == 'POST':
        # Check if email exists in BD
        email = request.POST['email']
        phone = request.POST['phone']
        if Registered_Data.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/login')
        elif Registered_Data.objects.filter(phone=phone).exists():
            messages.error(request, "Este teléfono ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/login')
        # ===========================
        else:
            if request.POST.get('username') \
                    and request.POST.get('first_name') \
                    and request.POST.get('password') \
                    and request.POST.get('phone') \
                    and request.POST.get('email') \
                    and request.POST.get('editorType') \
                    and request.POST.get('address') \
                    and request.POST.get('idTribute') \
                    and request.POST.get('editorPrefijo'):
                datos = request.POST.copy()
                if request.FILES:
                    # Convertir la imagen a base64 para poder serializarla a JSON en el request.session
                    datos['imagenProfile'] = base64.b64encode(request.FILES['imagenProfile'].read())
                    # Agregar la informacion inicial para que pueda ser leida por el "src" de <img> en el html
                    imagen_extension = request.FILES['imagenProfile'].content_type
                    datos['imagenProfile'] = f"data:{imagen_extension};base64," + datos['imagenProfile']
                confirmation_code = send_email(request)
                datos['code_confirmation'] = confirmation_code
                request.session['datos'] = datos
                return render(request, 'registration/email_confirmation.html')
            else:
                messages.error(request, "Complete todos los campos del formulario")
                return HttpResponseRedirect('/register_user')
    else:
        return render(request, 'registration/register_user.html')


def email_confirmation(request):
    if request.method == 'POST':
        if request.POST.get('code') != str(request.session.get('datos')['code_confirmation']):
            messages.error(request, 'Código incorrecto. Revise su correo electrónico')
            return HttpResponseRedirect('/email_confirmation')
        else:
            solicitud = Solicitud()
            solicitud.tipo = 'Solicitud-Inscripción'
            solicitud.status = 'Pendiente'
            solicitud.temporal = request.session.get('datos')
            solicitud.save()
            # LINEA PARA TRANSFORMAR DE BASE64 A IMAGE
            # PILImage.open(io.BytesIO(base64.b64decode(request.session.get('datos')['imagenProfile'])))
            messages.success(request, 'Su solicitud se ha enviado correctamente, le notificaremos a su correo '
                                      'cuando haya sido aceptada.')
            return HttpResponseRedirect('/')
    else:
        return render(request, 'registration/email_confirmation.html')

# ================= SECCIÓN DEL USUARIO (EDITOR) =================
# Function to render the Home Page for everybody
def frontend(request):
    return render(request, 'frontend.html')


# ================= SECCIÓN DEL USUARIO (ESPECIALISTA) =================
# Function to render editor's lists
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_editores(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_editor_list = Editor.objects.filter(
            Q(user__username__icontains=q) | Q(user__email__icontains=q) | Q(directions__icontains=q) |
            Q(note__icontains=q) | Q(user__first_name__icontains=q) | Q(type__icontains=q)
        ).order_by('-user__date_joined')
        if q.isnumeric():
            all_editor_list = Editor.objects.filter(Q(age=q) | Q(phone__contains=q) | Q(prefijo__value__contains=q) |
                                                    Q(id_tribute=q)).order_by('-user__date_joined')
    else:
        all_editor_list = Editor.objects.all().order_by('-user__date_joined')

    paginator = Paginator(all_editor_list, 4)
    page = request.GET.get('page')
    all_editor = paginator.get_page(page)

    return render(request, 'editores/editores-list.html', {"editores": all_editor})


# Function to render publication's lists
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_publicaciones(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_publication_list = Musical_Publication.objects.filter(
            Q(name__icontains=q) | Q(autor__icontains=q) | Q(editor__user__username__icontains=q) |
            Q(gender__icontains=q) | Q(ismn__icontains=q)
        ).order_by('-created_at')
    else:
        all_publication_list = Musical_Publication.objects.all().order_by('-created_at')

    paginator = Paginator(all_publication_list, 4)
    page = request.GET.get('page')
    all_publication = paginator.get_page(page)

    return render(request, 'publicaciones/publications-list.html', {"publicaciones": all_publication})


# Function to render las listas de solicitudes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_solicitudes(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_solicitudes_list = Solicitud.objects.filter(
            Q(tipo__icontains=q) | Q(editor__user__username__icontains=q) |
            Q(status__icontains=q)
        ).order_by('-created_at')
    else:
        all_solicitudes_list = Solicitud.objects.all().order_by('-created_at')

    paginator = Paginator(all_solicitudes_list, 4)
    page = request.GET.get('page')
    all_solicitudes = paginator.get_page(page)
    return render(request, 'solicitudes/solicitudes-list.html', {"solicitudes": all_solicitudes})


# Function to Add Editor
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def add_editor(request):
    if request.method == 'POST':

        # Check if email exist in BD
        email = request.POST['email']
        phone = request.POST['phone']
        if Registered_Data.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/backend')
        elif Registered_Data.objects.filter(phone=phone).exists():
            messages.error(request, "Este teléfono ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/backend')
        # ===========================
        else:
            if request.POST.get('username') \
                    and request.POST.get('first_name') \
                    and request.POST.get('password') \
                    and request.POST.get('phone') \
                    and request.POST.get('email') \
                    and request.POST.get('editorType') \
                    and request.POST.get('address') \
                    and request.POST.get('idTribute') \
                    and request.POST.get('editorPrefijo'):
                editor = Editor()
                user = User()
                user.username = request.POST.get('username')
                user.password = request.POST.get('password')
                user.first_name = request.POST.get('first_name')
                editor.phone = request.POST.get('phone')
                user.email = request.POST.get('email')
                editor.directions = request.POST.get('address')
                editor.type = request.POST.get('editorType')
                if editor.type == 'Independiente':
                    user.last_name = request.POST.get('last_name')
                    editor.age = request.POST.get('age')
                editor.directions = request.POST.get('address')
                editor.id_tribute = request.POST.get('idTribute')
                editor.user = user
                editor.prefijo = generate_prefijo_editor(request.POST.get('editorPrefijo'))
                editor.note = request.POST.get('note')
                editor.image_profile = request.FILES.get('imagenProfile')
                user.save()
                editor.save()

                # Register email and phone inside BD
                contact = Registered_Data()
                contact.email = email
                contact.phone = phone
                contact.save()
                # ========================

                messages.success(request, "Editor añadido correctamente !")
                return HttpResponseRedirect('/backend')
    else:
        return render(request, "editores/add.html")


# Function to delete Editor
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_editor(request, editor_id):
    editor = Editor.objects.get(id=editor_id)
    Registered_Data.objects.get(phone=editor.phone).delete()
    User.objects.get(username=editor.user.username).delete()
    editor.delete()
    messages.success(request, "Editor eliminado correctamente !")
    return HttpResponseRedirect('/backend')


# Function to access the Editor individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def editor(request, editor_id):
    editor = Editor.objects.get(id=editor_id)
    if editor:
        return render(request, "editores/edit.html", {"editor": editor})
    else:
        return HttpResponseRedirect('/backend')


# Function to edit the Editor
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_editor(request):
    if request.method == "POST":
        editor = Editor.objects.get(id=request.POST.get('id'))
        if editor:
            editor.user.username = request.POST.get('username')
            editor.user.first_name = request.POST.get('first_name')
            editor.phone = request.POST.get('phone')
            editor.user.email = request.POST.get("email")
            editor.directions = request.POST.get('address')
            editor.type = request.POST.get("editorType")
            if request.POST.get('age'):
                editor.age = request.POST.get("age")
                editor.user.last_name = request.POST.get('last_name')
            editor.id_tribute = request.POST.get("idTribute")
            editor.note = request.POST.get("note")
            editor.image_profile = request.FILES.get('imagenProfile')
            editor.save()
            messages.success(request, "Editor editado correctamente !")
            return HttpResponseRedirect('/backend')


# Function to show musical collections
def musical_colections_list(request):
    Musical_Collections_Objects = Musical_Publication.objects.all()
    data = {
        'publicaciones_musicales': Musical_Collections_Objects,
    }

    if not Musical_Collections_Objects:
        data['mensaje'] = "No hay publicaciones musicales en el sistema"
        return render(request, 'colecciones-musicales.html', data)
    elif 'q' in request.GET:
        q = request.GET['q']
        data['publicaciones_musicales'] = Musical_Publication.objects.filter(
            Q(name__icontains=q) | Q(autor__icontains=q) | Q(gender__icontains=q)
        )
        if not data['publicaciones_musicales']:
            data['mensaje'] = "No hay coincidencias"
    return render(request, 'colecciones-musicales.html', data)


# Function to add a musical publication
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def add_musical_publication(request):
    if request.method == 'POST':
        if request.POST.get('title') \
                and request.POST.get('autor') \
                and request.POST.get('editor') \
                and request.POST.get('prefijo-publicacion') \
                and request.POST.get('ismn') \
                and request.POST.get('gender') \
                and request.POST.get('date'):
            musical_publication = Musical_Publication()
            editor = Editor.objects.get(user__first_name=request.POST.get('editor'))
            prefijo_value = request.POST.get('prefijo-publicacion').rpartition(" ")[2]
            prefijo = generate_prefijo_publicacion(prefijo_value)
            musical_publication.name = request.POST.get('title')
            musical_publication.autor = request.POST.get('autor')
            musical_publication.editor = editor
            musical_publication.prefijo = prefijo
            musical_publication.ismn = request.POST.get('ismn')
            musical_publication.gender = request.POST.get('gender')
            musical_publication.letra = request.FILES.get('publication_letter')
            if request.FILES.get('publication_image'):
                musical_publication.imagen = request.FILES.get('publication_image')
            else:
                pass
            musical_publication.description = request.POST.get('note')
            musical_publication.date_time = request.POST.get('date')
            musical_publication.save()
            messages.success(request, "Publicación musical añadida correctamente !")
            return HttpResponseRedirect('/backend_publicaciones')
    else:
        editores = Editor.objects.annotate(Count('musical_publication'))
        data = {'editores': editores}
        return render(request, "publicaciones/add_publication.html", data)


# Function to access the musical_publication individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def musical_publication(request, musical_publication_id):
    musical_publication = Musical_Publication.objects.get(id=musical_publication_id)
    editores = Editor.objects.all()
    data = {"musical_publication": musical_publication, "editores": editores}
    if musical_publication:
        return render(request, "publicaciones/edit_publication.html", data)


# Function to edit the patients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_musical_publication(request):
    if request.method == "POST":
        musical_publication = Musical_Publication.objects.get(id=request.POST.get('id'))
        if musical_publication:
            musical_publication.name = request.POST.get('title')
            musical_publication.autor = request.POST.get('autor')
            if request.POST.get('editor') != str(musical_publication.editor):
                editor = Editor.objects.get(user__first_name=request.POST.get('editor'))
                musical_publication.editor = editor
                prefijo_value = request.POST.get('prefijo-publicacion').rpartition(" ")[2]
                prefijo = generate_prefijo_publicacion(prefijo_value)
                musical_publication.prefijo = prefijo
                musical_publication.ismn = request.POST.get('ismn')
            else:
                pass
            musical_publication.gender = request.POST.get('gender')
            if request.FILES.get('publication_letter'):
                musical_publication.letra = request.FILES.get('publication_letter')
            else:
                pass
            if request.FILES.get('publication_image'):
                musical_publication.imagen = request.FILES.get('publication_image')
            else:
                pass
            musical_publication.description = request.POST.get('note')
            musical_publication.date_time = request.POST.get('date')
            musical_publication.save()
            messages.success(request, "Publicacion Musical actualizada correctamente !")
            return HttpResponseRedirect('/backend_publicaciones')


# Function to delete a musical publication
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_musical_publication(request, musical_publication_id):
    musical_publication = Musical_Publication.objects.get(id=musical_publication_id)
    musical_publication.delete()
    messages.success(request, "Publicacion Musical eliminada correctamente !")
    return HttpResponseRedirect('/backend_publicaciones')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_solicitud(request, solicitud_id):
    solicitud = Solicitud.objects.get(id=solicitud_id)
    solicitud.delete()
    messages.success(request, "Solicitud eliminada correctamente !")
    return HttpResponseRedirect('/backend_solicitudes')


# Function to send Confirmation Code
def generate_confirmation_code():
    return randint(1000, 9999)


def send_email(request):
    confirmation_code = generate_confirmation_code()
    context = {
        'nombre': request.POST.get('first_name'),
        'code': confirmation_code
    }
    message = loader.render_to_string('mail_confirmation_client.html', context)
    email = EmailMultiAlternatives(
        "Confirmación de Correo", message,
        "CCL de Cuba",
        [request.POST.get('email')],
    )
    email.content_subtype = 'html'
    try:
        email.send()
        return confirmation_code
    except TimeoutError or SMTPServerDisconnected:
        messages.error('Error en la conexión. Intente más tarde.')
        return HttpResponseRedirect('/')


def export_musical_publication(request, musical_publication_id):
    # Tomar la Info. de la Publicación a exportar
    publication = Musical_Publication.objects.get(id=musical_publication_id)

    # Crear el temporal para el pdf
    buffer = io.BytesIO()

    # Importar las fuentes externas
    pdfmetrics.registerFont(TTFont('RobotoCondensed-Bold', 'fonts/RobotoCondensed-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoSlab', 'fonts/RobotoSlab-VariableFont_wght.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Italic', 'fonts/RobotoCondensed-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto', 'fonts/RobotoCondensed-Regular.ttf'))

    PAGE_WIDTH, PAGE_HEIGHT = A4
    style_letra = ParagraphStyle(name='letra_style', rightIndent=25, fontName="Roboto")
    style_description = ParagraphStyle(name='description_style', rightIndent=15, leading=15, fontName="Roboto")
    letra = Paragraph(f'<u><a href="http://127.0.0.1:8000/{publication.letra.url}" '
                      f'color="blue">http://127.0.0.1:8000/{publication.letra.url}</a></u>', style_letra)
    if publication.description:
        descripcion = Paragraph(f'<font name="RobotoCondensed-Bold" '
                                f'color={colors.Color(0.21, 0.25, 0.33)}>DESCRIPCIÓN</font>'
                                f'<br/><font color={colors.Color(0.21, 0.25, 0.33)}>{publication.description}</font>',
                                style_description)
    else:
        descripcion = Paragraph(f'<font name="RobotoCondensed-Bold" '
                                f'color={colors.Color(0.21, 0.25, 0.33)}>DESCRIPCIÓN</font>'
                                f'<br/>'
                                f'<font name="Roboto-Italic" size=8 color={colors.Color(0.49, 0.30, 0.34)}>'
                                f'(Descripción opcional de la obra, breve historia de su realización y datos adicionales)</font>',
                                style_description)
    data = [['AUTOR', publication.autor],
            ['NOMBRE', publication.name],
            ['GÉNERO', publication.gender],
            ['EDITOR', publication.editor],
            ['LETRA DE LA CANCIÓN', letra, ''],
            ['ISMN', publication.ismn, descripcion],
            ['PREFIJO', publication.prefijo, ''],
            ['FECHA DE PUBLICACIÓN', publication.created_at.date(), ''],
            ['FECHA DE REALIZACIÓN', publication.date_time, ''],
            ['DERECHOS DE AUTOR', 'EN VENTA', '']
            ]

    def myPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, 600, 900, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, 810, 600, 50, stroke=0, fill=1)
        # Imprimir el Logo de la empresa
        canvas.drawImage('media/logo.jpg', (PAGE_WIDTH - 80) / 2, 685, 80, 110)
        # Crear encabezado del reporte
        publication_info_textobject = canvas.beginText()
        texto_encabezado = 'INFORMACIÓN DE LA PUBLICACIÓN'
        width_texto_encabezado = canvas.stringWidth(texto_encabezado, 'RobotoCondensed-Bold', 15)
        origin_start = (PAGE_WIDTH - width_texto_encabezado) / 2
        publication_info_textobject.setTextOrigin(origin_start, 665)
        publication_info_textobject.setFont('RobotoCondensed-Bold', 15)
        publication_info_textobject.setFillColorRGB(0.21, 0.25, 0.33)
        publication_info_textobject.setCharSpace(0.4)
        publication_info_textobject.textLine(texto_encabezado)
        # Titulo de la publicacion
        width_title_publicaction = canvas.stringWidth(publication.name, 'RobotoSlab', 30)
        origin_start = PAGE_WIDTH / 2 - width_title_publicaction / 2
        publication_info_textobject.setTextOrigin(origin_start, 626)
        publication_info_textobject.setFont('RobotoSlab', 30)
        publication_info_textobject.setFillColorRGB(0.49, 0.30, 0.34)
        publication_info_textobject.textLine(publication.name)
        canvas.drawText(publication_info_textobject)
        # Raya separadora
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(50, 600, 500, 4, stroke=0, fill=1)
        # Content
        publication_detail = canvas.beginText()
        publication_detail.setTextOrigin(50, 560)
        publication_detail.setFont('RobotoCondensed-Bold', 11)
        publication_detail.setCharSpace(0.25)
        publication_detail.setFillColorRGB(0.21, 0.25, 0.33)
        publication_detail.textLine('DETALLES Y AUTORÍA')
        canvas.drawText(publication_detail)
        # **--Primera Tabla - Autoria--**
        table_autoria = Table(data[:4], colWidths=[50, 400])
        table_autoria_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                          ('FONT', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
                                          ('FONT', (1, 0), (1, -1), 'Roboto'),
                                          ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
                                          ('LINEBEFORE', (1, 0), (1, -1), 0, colors.Color(1, 0, 0, alpha=0)),
                                          # ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                          # ('LINEABOVE', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34))
                                          ])
        table_autoria.setStyle(table_autoria_style)
        table_autoria.wrapOn(canvas, 50, 475)
        table_autoria.drawOn(canvas, 50, 475)
        # **--Segunda Tabla - Descripcion--**
        # Encabezado
        publication_detail.setTextOrigin(50, 448)
        publication_detail.textLine('DESCRIPCIÓN DE LA OBRA')
        canvas.drawText(publication_detail)
        # Tabla Descripción
        table_description_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                              ('VALIGN', (0, -1), (1, -1), 'TOP'),
                                              ('VALIGN', (-1, 1), (-1, 1), 'TOP'),
                                              ('TOPPADDING', (-1, 1), (-1, 1), 5),
                                              ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                                              ('FONT', (0, 0), (-1, -1), 'Roboto'),
                                              ('FONT', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
                                              ('FONT', (1, 5), (1, 5), 'RobotoCondensed-Bold'),
                                              ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
                                              ('LINEBEFORE', (1, 0), (1, -1), 0, colors.Color(1, 0, 0, alpha=0)),
                                              ('LINEBEFORE', (1, 5), (1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('BOX', (0, 1), (1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('LINEABOVE', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('SPAN', (1, 0), (2, 0)),
                                              ('SPAN', (2, 1), (2, -1))
                                              ])

        table_description = Table(data[4:], colWidths=[120, 120, 260], rowHeights=[None, None, None, None, None, 70])
        table_description.setStyle(table_description_style)
        w, h = table_description.wrapOn(canvas, 50, 275)
        x_coord_table_description = 50
        y_coord_table_description = 435 - h
        table_description.drawOn(canvas, x_coord_table_description, y_coord_table_description)
        # CheckBoxes
        x_checkbox = 57
        y_checkbox = y_coord_table_description + 30
        canvas.acroForm.checkbox(x=x_checkbox, y=y_checkbox, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34), borderWidth=0.5)
        canvas.acroForm.checkbox(x=x_checkbox, y=y_checkbox - 16, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34, alpha=0.1), borderWidth=0.5)
        canvas.acroForm.checkbox(x=x_checkbox + 120, y=y_checkbox, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34), borderWidth=0.5)
        canvas.acroForm.checkbox(x=x_checkbox + 120, y=y_checkbox - 16, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34, alpha=0.1), borderWidth=0.5)
        options = canvas.beginText()
        # Opciones 'privado y publico' de "Derechos de Autor"
        # Publico
        options.setTextOrigin(x_checkbox + 15, y_checkbox + 3)
        options.setFont('Roboto', 10)
        options.textLine('público')
        canvas.drawText(options)
        # Privado
        options.setTextOrigin(x_checkbox + 15, y_checkbox - 12)
        options.textLine('privado')
        canvas.drawText(options)
        # Opciones si y no de 'EN VENTA'
        # Si
        options.setTextOrigin(x_checkbox + 135, y_checkbox + 3)
        options.textLine('si')
        canvas.drawText(options)
        # No
        options.setTextOrigin(x_checkbox + 135, y_checkbox - 12)
        options.textLine('no')
        canvas.drawText(options)

        # Cover de la publicacion
        def redondear_imagen(imagen, radio):
            # Crear una máscara redonda del mismo tamaño que la imagen
            mascara = PILImage.new("L", imagen.size, 0)
            dibujo = ImageDraw.Draw(mascara)
            dibujo.ellipse((0, 0, imagen.width, imagen.height), fill=255)

            # Crear una nueva imagen con fondo transparente
            imagen_redonda = PILImage.new("RGBA", imagen.size, (0, 0, 0, 0))

            # Pegar la imagen original en la nueva imagen usando la máscara
            imagen_redonda.paste(imagen, mask=mascara)

            # Crear una nueva máscara redonda con un borde transparente
            borde = PILImage.new("L", imagen.size, 0)
            dibujo_borde = ImageDraw.Draw(borde)
            dibujo_borde.ellipse(
                (radio, radio, imagen.width - radio, imagen.height - radio), fill=255
            )

            # Pegar la imagen redonda en una nueva imagen con el borde
            imagen_final = PILImage.new("RGBA", imagen.size, (0, 0, 0, 0))
            imagen_final.paste(imagen_redonda, mask=borde)

            return imagen_final

        # Abrir la imagen original
        imagen_original = PILImage.open(publication.imagen.path)

        # Radio del borde redondeado
        radio_borde = 5

        # Redondear la imagen
        imagen_redondeada = redondear_imagen(imagen_original, radio_borde)

        # Guardar la imagen redondeada
        imagen_redondeada.save(f"App/static/img/imagen_redondeada.png")

        cover = Image("App/static/img/imagen_redondeada.png", width=150, height=120)
        w, h = cover.wrapOn(canvas, 350, 120)
        cover.drawOn(canvas, 350, y_coord_table_description - h - 20)

        # Text url from cover
        cover_style = ParagraphStyle(name='style', fontName="Roboto")
        cover_url = Paragraph(f'<u><a href="http://127.0.0.1:8000/{publication.imagen.url}" '
                              f'color="blue">Mostrar Imagen</a></u>', cover_style)
        w = canvas.stringWidth('Mostrar Imagen', 'Roboto', 10)
        cover_url.wrapOn(canvas, 88, 12)
        cover_url.drawOn(canvas, 424 - w / 2, 110)

        # Texto Informativo
        text_info_style = ParagraphStyle(name='text_info_style')
        text_info = Paragraph(f'<font name="Roboto-Italic" size=8 color={colors.Color(0.49, 0.30, 0.34)}>'
                              f'El reciente documento que muestra los datos principales de la publicación musical '
                              f'emerge como una herramienta esencial para el equipo y las partes interesadas. '
                              f'Al encapsular la inspiración artística, la partitura, descripción y '
                              f'datos biográficos, sirve como guía integral para comprender y comunicar '
                              f'el proyecto de publicación. Este recurso clave garantiza un impacto positivo en todos '
                              f'los aspectos de la iniciativa musical, y se espera compartir más detalles en el futuro.</font>',
                              text_info_style)
        w, h = text_info.wrapOn(canvas, 200, 200)
        y_coord_text_info = y_coord_table_description - h - 20
        text_info.drawOn(canvas, 50, y_coord_text_info)

        # Tabla de Reportado por:
        # Datos
        if request.user.especialista:
            departamento = 'Informatica - CCL'
        else:
            departamento = '-'
        data_table_report_by = [
            ['REPORTADO POR:', ''],
            ['Nombre:', request.user.first_name],
            ['Fecha:', datetime.today().date()],
            ['Departamento:', departamento]
        ]
        report_by_style = TableStyle(
            [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('ALIGN', (1, 0), (1, -1), 'CENTER'),
             ('FONTNAME', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
             ('FONTNAME', (1, 0), (1, -1), 'Roboto'),
             ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
             ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34))]
        )
        table_report_by = Table(data_table_report_by, colWidths=[100, 140], style=report_by_style)
        w, h = table_report_by.wrapOn(canvas, 400, 200)
        table_report_by.drawOn(canvas, 50, y_coord_text_info - h - 15)

        # Footer
        # Raya separadora
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(50, 50, 500, 4, stroke=0, fill=1)
        # Barra final
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, 0, 600, 10, stroke=0, fill=1)
        canvas.restoreState()

    story = [Paragraph('')]
    doc = SimpleDocTemplate(buffer)
    doc.build(story, onFirstPage=myPage)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{publication.name}.pdf")


def crear_listas():
    lista_imagenes, lista_titulos, lista_descripciones = [], [], []
    imagenes_root = Path(Path.home(), 'Desktop\Caratulas Estrenos\Animados')
    descripcion_root = Path(Path.home(), 'Desktop\Caratulas Estrenos\Animados\Descripciones.txt')
    lista_descripciones = open(descripcion_root, encoding='utf-8').readlines()
    for img in Path(imagenes_root).glob("*.jpg"):
        lista_imagenes.append(str(img))
        lista_titulos.append(img.stem)

    return lista_imagenes, lista_titulos, lista_descripciones


def export_catalogo_peliculas(request, musical_publication_id):
    pdfmetrics.registerFont(TTFont('RobotoCondensed-Bold', 'fonts/RobotoCondensed-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Action', 'fonts/Super_Sedan.ttf'))
    PAGE_WIDTH, PAGE_HEIGHT = letter
    buffer = io.BytesIO()
    img_list, title_list, description_list = crear_listas()
    titulo_catalogo = 'Animados'

    def myFirstPage(canvas, doc):
        canvas.saveState()

        def draw(x=0, y=0, counter=0):
            if y < PAGE_HEIGHT:
                if x < PAGE_WIDTH:
                    canvas.drawImage(img_list[counter], x, y, 100, 120)
                    counter += 1
                    x += 100
                    draw(x, y, counter)
                else:
                    y += 120
                    x = 0
                    draw(x, y, counter)
            else:
                return

        draw()

        font_size = 90
        style_title1 = ParagraphStyle(name='style_title1', fontName='Action', fontSize=font_size,
                                      textColor=colors.red)
        title = Paragraph(titulo_catalogo, style_title1)
        w_title, h_title = title.wrapOn(canvas, PAGE_WIDTH, PAGE_HEIGHT)
        canvas.rotate(45)
        canvas.setFillColorRGB(1, 1, 1)
        canvas.rect(260, 200, w_title - 65, -90, stroke=0, fill=1)
        title.drawOn(canvas, 270, 200)
        canvas.rotate(-45)
        canvas.restoreState()

    def myLaterPage(canvas, doc):
        canvas.saveState()
        canvas.drawString(inch, 0.75 * inch, "Page %s" % (doc.page - 1))
        canvas.restoreState()

    def build_doc(pbuffer):
        # Datos para conformar el documento
        doc = SimpleDocTemplate(pbuffer)
        story = [Spacer(0, 8 * inch)]
        # Datos para la tabla
        datas = []
        counter = 0
        fila_title = 0
        fila1_imagen = 0
        fila2_imagen = 1
        fila3_imagen = 2
        fila4_imagen = 3
        fila1_description = 1
        fila2_description = 2
        fila3_description = 3
        style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('INNERGRID', (1, 0), (1, -1), 1, colors.black),
                            ('BOX', (1, 0), (1, -1), 1, colors.black)
                            ])
        style_title = ParagraphStyle(name='style_title', fontName='RobotoCondensed-Bold',
                                     fontSize=14, alignment=1)
        style_description = ParagraphStyle(name='style_descrption', fontName='Helvetica-Bold',
                                           fontSize=12, alignment=4)

        # For para llenar los datos de la tabla
        for img in img_list:
            title = Paragraph(title_list[counter].upper(), style_title)
            descripcion = Paragraph(description_list[counter], style_description)
            # Matriz de Datos para la tabla
            datas.append([Image(img, 150, 155), title])
            datas.append(['', descripcion])
            datas.append(['', ''])
            datas.append(['', ''])
            counter += 1
            # Style Table
            # Title
            style.add('VALIGN', (1, fila_title), (1, fila_title), 'MIDDLE')
            style.add('BACKGROUND', (1, fila_title), (1, fila_title), colors.lightsteelblue)
            # Imagen
            style.add('VALIGN', (0, fila1_imagen), (0, fila1_imagen), 'TOP')
            style.add('SPAN', (0, fila1_imagen), (0, fila2_imagen))
            style.add('SPAN', (0, fila1_imagen), (0, fila3_imagen))
            style.add('SPAN', (0, fila1_imagen), (0, fila4_imagen))
            style.add('TOPPADDING', (0, fila1_imagen), (0, fila1_imagen), 0)

            # Description
            style.add('SPAN', (1, fila1_description), (1, fila2_description))
            style.add('SPAN', (1, fila1_description), (1, fila3_description))
            style.add('VALIGN', (1, fila1_description), (1, fila1_description), 'TOP')
            style.add('ALIGN', (1, fila1_description), (1, fila1_description), 'LEFT')
            style.add('LEADING', (1, fila1_description), (1, fila1_description), 17)
            # Siguientes filas de la tabla
            fila_title += 4
            fila1_imagen += 4
            fila2_imagen += 4
            fila3_imagen += 4
            fila4_imagen += 4
            fila1_description += 4
            fila2_description += 4
            fila3_description += 4

        # TABLE
        table = Table(datas, colWidths=(170, 335))
        table.setStyle(style)
        story.append(table)
        doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPage)

    build_doc(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"CATÁLOGO_DE_PELICULAS_{titulo_catalogo}.pdf")


