from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Path to render the Homepage
    path('', views.frontend, name="frontend"),
    # Path Login/Logout/Register
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('email_confirmation/', views.email_confirmation, name='email_confirmation'),
    # ===============
    # BACKEND SECTION
    # ===============
    # Path to access the backend page
    path('backend/', views.backend_editores, name="backend_editores"),
    path('backend_publicaciones', views.backend_publicaciones, name="backend_publicaciones"),
    path('backend_solicitudes', views.backend_solicitudes, name="backend_solicitudes"),
    # Path to add an editor
    path('add_editor/', views.add_editor, name="add_editor"),
    # Path to delete an editor
    path('delete_editor/<str:editor_id>', views.delete_editor, name="delete_editor"),
    # Path to access the editor individualy
    path('editor/<str:editor_id>', views.editor, name="editor"),
    # Path to edit the editor
    path('edit_editor/', views.edit_editor, name="edit_editor"),
    # Path to access the musical colections
    path('musical_colections/', views.musical_colections_list, name="musical_colections"),
    # Path to add a musical publication
    path('add_musical_publicaton/', views.add_musical_publication, name="add_musical_publicaction"),
    # Path to access the muscial publication individually
    path('musical_publication/<str:musical_publication_id>', views.musical_publication, name="musical_publication"),
    # Path to edit the musical publication
    path('edit_musical_publication/', views.edit_musical_publication, name="edit_musical_publication"),
    # Path to delete a Musical_Publication
    path('delete_musical_publication/<str:musical_publication_id>', views.delete_musical_publication, name="delete_musical_publication"),
    # Path to delete a Solicitud
    path('delete_solicitud/<str:solicitud_id>', views.delete_solicitud, name="delete_solicitud"),

    # ========================== EXPORT DOCUMENTS ==========================
    # Path to export a single musical publication
    path('export_musical_publication/<str:musical_publication_id>', views.export_musical_publication, name="export_publication"),

    # ========================== SEND EMAIL ==========================
    # Path to send confirmation-code
    path('send_email', views.send_email, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)