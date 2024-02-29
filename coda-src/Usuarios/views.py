from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import Usuario, Tutor, Alumno, Coda, Cordinador
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .constants import TUTOR, ALUMNO, COORDINADOR,CODA, TEMPLATES
from django.views.generic.list import ListView
from django.http import HttpResponseBadRequest
from django.views.generic import View
from . import forms as userForms

# Create your views here.

class ContextConRolesMixin:

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_rol = self.request.user.get_rol()
        if user_rol == ALUMNO:
            context["header_footer"] = TEMPLATES[ALUMNO]
        elif user_rol == TUTOR:
            context["header_footer"] = TEMPLATES[TUTOR]
        elif user_rol == COORDINADOR:
            context["header_footer"] = TEMPLATES[COORDINADOR]
        elif user_rol == CODA:
            context["header_footer"] = TEMPLATES[CODA]
        return context

class ContextNotificationsMixin:

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = Usuario.objects.get(pk=self.request.user.pk)
        notifications_raw = user.notifications.unread()
        unread_notifications = []

        for notification in notifications_raw:
            notificacion_temp = {}
            notificacion_temp["header"] =  "Notificacion" if not notification.description else f"{notification.description}"
            notificacion_temp["text"] = f'{notification.verb} por {Usuario.objects.get(matricula=notification.actor).get_full_name()}'
            
            notificacion_temp["time"] = notification.timestamp
            #remitente = 
            #notificacion_temp["origen"] = f'{}'
            unread_notifications.append(notificacion_temp)
            

       
        context["notificaciones_list"] = unread_notifications
        return context


# TODO Remove test views
def login_view_test(request):

    return render(request, 'Usuarios/login.html')

def perfil_view_test(request):

    return render(request, 'Usuarios/perfil.html')

def recordarcontras_view_test(request):

    return render(request, 'Usuarios/recordarContrasenia.html')



class PerfilAlumnoView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin, DetailView):

    model = Alumno
    template_name = 'Usuarios/perfil_alumno.html'
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        return context

class PerfilTutorView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin, DetailView):

    model = Tutor
    template_name = 'Usuarios/perfil_tutor.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()

@login_required
def redirect_perfil(request):

    if Tutor.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-tutor', pk=request.user.pk)
    
    if Alumno.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-alumno', pk=request.user.pk)
    if Coda.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-coda', pk=request.user.pk)
    if Cordinador.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-cordinador', pk=request.user.pk)
    
    return redirect('perfil-alumno', pk=request.user.pk)

class PerfilCodaView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin, DetailView):

    model = Coda
    template_name = 'Usuarios/perfil_cooda.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
    

class PerfilCordinadorView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin, DetailView):

    model = Cordinador
    template_name = 'Usuarios/perfil_cordinador.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()

@login_required
def redirect_perfil(request):

    if Tutor.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-tutor', pk=request.user.pk)
    
    if Alumno.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-alumno', pk=request.user.pk)
    if Coda.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-coda', pk=request.user.pk)
    if Cordinador.objects.filter(pk=request.user.pk).exists():
        return redirect('perfil-cordinador', pk=request.user.pk)
    
    
    return redirect('perfil-alumno', pk=request.user.pk)
    

# TODO Eliminar para prod
class DebugTutoriasView(LoginRequiredMixin, ListView):

    model = Tutor
    template_name='Tutorias/verTutorias_coordinador.html'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
    

class UsuarioLoginView(LoginView):

    redirect_authenticated_user = True

    template_name = "Usuarios/login.html"
    
    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def login_success(request):
    """
    Redirecciona los usuarios a su view correspondiente
    """


    if Alumno.objects.filter(pk=request.user.pk).exists():
        return redirect('Tutorias-alumno')
    
    if Tutor.objects.filter(pk=request.user.pk).exists():
        return redirect('Tutorias-tutor')
    if Cordinador.objects.filter(pk=request.user.pk).exists():
        return redirect('Tutorias-cordinador')
    if Coda.objects.filter(pk=request.user.pk).exists():
        return redirect('Tutorias-Coda')
    
    print('ERROR: Usuario no definido')
    return HttpResponseBadRequest("ERROR. Tipo de usuario no definido")
    #return redirect()
    # if Usuario.objects.filter(pk=request.user.pk).exists:
    #     return redirect('Tutorias-coordinador')

class ChangePasswordView(LoginRequiredMixin, ContextConRolesMixin, PasswordChangeView):
    template_name = 'Usuarios/change_password.html'  # Create a template for password change form
    success_url = reverse_lazy('password_change_done')  # Redirect to this URL after a successful password change

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context

class PasswordChangeDoneView(TemplateView):
    template_name = 'Usuarios/password_change_done.html'

class BorrarNotificaciones(View):
    def post(self, request):
        usuario = Usuario.objects.get(pk=self.request.user.pk)
        notificaciones = usuario.notifications.unread()
        notificaciones.mark_all_as_read()


        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# Conjunto de Views Para Agregar usuarios

#PermissionRequiredMixin
class CreateAlumnoView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin,  CreateView):

    template_name = 'Usuarios/agregar_alumno.html'
    success_url = reverse_lazy('login_success')
    #model = Alumno
    form_class = userForms.FormAlumno
    permission_required="Usuarios.add_Alumno"
    
#PermissionRequiredMixin
class CreateCordinadorView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin,  CreateView):
    template_name = 'Usuarios/agregar_cordinador.html'
    success_url = reverse_lazy('login_success')
    #model = Cordinador
    form_class = userForms.FormCordinador
    permission_required="Usuarios.add_Cordinador"
    
#PermissionRequiredMixin
class CreateTutorView(LoginRequiredMixin, ContextNotificationsMixin, ContextConRolesMixin,  CreateView):
    template_name = 'Usuarios/agregar_tutor.html'
    success_url = reverse_lazy('login_success')
    #model = Tutor
    form_class = userForms.FormTutor
    permission_required="Usuarios.add_Tutor"
    


# class AceptarTutoriaView(View):
#     def post(self, request, pk):
#         tutoria = get_object_or_404(Tutoria, pk=pk)
#         tutoria.estado = ACEPTADO
#         tutoria.save()
#         return redirect('Tutorias-tutor')  