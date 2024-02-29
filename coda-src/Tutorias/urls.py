from django.urls import path

from . import views


urlpatterns = [
    #path('', views.index, name='index'),
    # path("vertutorias/", views.ver_tutorias),
    # path("editartutoria/", views.editar_tutoria),
    # path("solicitudtutoria/", views.solicitud_tutoria),
    #path('', views.index, name='index'),
    path('tutorias/<int:pk>/', views.TutoriasDetailView.as_view(), name='Tutorias-detail'),
    path('editar-tutoria/<int:pk>', views.TutoriaUpdateView.as_view(), name='Tutorias-update'),
    path('crear-tutoria/', views.TutoriaCreateView.as_view(), name='Tutorias-create'),
    path('crear-tutoria/<int:pk_alumno>/', views.CrearTutoriaPorAlumnoView.as_view(), name='crear-tutoria'),
    
    path('historial-tutorias/', views.HistorialTutoriasListView.as_view(), name='Tutorias-historial'),
    path('tutorias-alumno/', views.VerTutoriasAlumnoListView.as_view(), name='Tutorias-alumno'),
    path('tutorias-cordinador/', views.VerTutoriasCordinadorListView.as_view(), name='Tutorias-Cordinador'),
    path('tutorias-coda/', views.VerTutoriasCodaListView.as_view(), name='Tutorias-Coda'),
    path('tutorados-tutor/', views.VerTutoradosTutorListView.as_view(), name='Tutorados-tutor'),
    path('tutorias-tutor/', views.VerTutoriasTutorListView.as_view(),name='Tutorias-tutor'),
    path('tutoria/<int:pk>/aceptar/', views.AceptarTutoriaView.as_view(), name='aceptar_tutoria'),
    path('tutoria/<int:pk>/rechazar/', views.RechazarTutoriaView.as_view(), name='rechazar_tutoria'),
    path('debug-tutorias/', views.DebugTutoriasView.as_view(), name='debug-tutorias'),
    #path('reset-password/', views.DebugTutoriasView.as_view(), name='reset_password'),
    
    path('tutoria-rapida/', views.QuickCreateTutoriaView.as_view(), name='tutoria-rapida'),
    path('qr-code/', views.QRCodeView.as_view(), name='qr-code'),
    # Desactivamos la tutoria por tutor mientras se arregla la coordinacion de horarios
    #path('creartutoria/<int:pk_alumno>/', views.CrearTutoriaPorAlumnoView.as_view(),name='crear-tutoria-por-alumno'),
]