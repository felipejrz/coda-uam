from typing import Any, Dict
from django.shortcuts import get_object_or_404, redirect
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.urls import reverse_lazy
from django.utils.text import slugify
import qrcode
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from datetime import datetime

from .models import Tutoria, Tutor, Alumno
from .forms import FormTutorias
from .constants import PENDIENTE, ACEPTADO, RECHAZADO
from Usuarios.constants import TUTOR, ALUMNO, COORDINADOR, TEMPLATES, CORREO
from Usuarios.views import BaseAccessMixin, CodaViewMixin, TutorViewMixin, AlumnoViewMixin, CordinadorViewMixin
from notifications.signals import notify
from smtplib import SMTPException

# Create your views here.
def index(request):
    return HttpResponse("Tutorias app index placeholder")

class AceptarTutoriaView(View):
    def post(self, request, pk):
        tutoria = get_object_or_404(Tutoria, pk=pk)
        tutoria.estado = ACEPTADO
        tutoria.save()
        return redirect('Tutorias-tutor')  

class RechazarTutoriaView(View):
    def post(self, request, pk):
        tutoria = get_object_or_404(Tutoria, pk=pk)
        tutoria.estado = RECHAZADO
        tutoria.save()
        return redirect('Tutorias-tutor')    
    
class TutoriaUpdateView(BaseAccessMixin, UpdateView):
    model = Tutoria
    fields = ['tema', 'fecha', 'descripcion']

    success_url  = reverse_lazy('Tutorias-historial')

    template_name = 'Tutorias/editarTutoria.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rol = self.request.user.get_rol()
        if rol == TUTOR:
             tutor = Tutor.objects.get(pk=self.request.user)
        recipient = Alumno.objects.filter(pk=self.get_object().alumno)

        notify.send(tutor, recipient=recipient, verb='Tutoria Modificada')
        return super().form_valid(form)
    
    
# Solicitud Tutorias
class TutoriaCreateView(AlumnoViewMixin, CreateView):
    #model = Tutoria
    #fields = ['tema', 'fecha', 'descripcion']

    form_class = FormTutorias

    template_name = 'Tutorias/solicitudTutoria.html'

    success_url = reverse_lazy('Tutorias-alumno')

    def form_valid(self, form: FormTutorias) -> HttpResponse:
        alumno = get_object_or_404(Alumno, pk=self.request.user)
        form.instance.alumno = alumno
        form.instance.tutor = alumno.tutor_asignado

        rol = self.request.user.get_rol()
        if rol == ALUMNO:
            recipient = Tutor.objects.get(pk=alumno.tutor_asignado)

        notify.send(alumno, recipient=recipient, verb='Nueva solicitud de tutoria', description=f'{form.instance.get_tema_display()}')
        
        # TODO utilizar una rutina para mandar los correos
        #send_mail(
         #   subject='Nueva solicitud de tutoria',
          #  message=f'Solicitud de tutoria creada por {alumno.get_full_name()} con tema: {form.instance.get_tema_display()}',
           # from_email=CORREO,
            #recipient_list=[recipient.email],
            #fail_silently=False
    
        

        return super().form_valid(form)

    def get_initial(self) -> dict[str, Any]:
        return super().get_initial()
    


# Ver Tutorias
# TODO Añadir verificación de permisos de acceso a la tutoria
class TutoriasDetailView(BaseAccessMixin, DetailView):
     
    model = Tutoria

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

    template_name='Tutorias/verTutorias_tutor.html'

    def get_queryset(self) -> QuerySet[Any]:
        
        if Tutor.objects.filter(pk=self.request.user.pk).exists():
            # Tutorias correspondientes al tutor
            queryset = super().get_queryset().filter(tutor=self.request.user)
        else: 
            # Tutorias correspondientes al alumno
            queryset = super().get_queryset().filter(alumno=self.request.user)
        
        if self.request.user.is_superuser == 1: 
            # Muestra todas las tutorias para el primer usuario creado (generalmente el primer superuser)
            queryset = super().get_queryset().all()
        
        return queryset
    
class HistorialTutoriasListView(BaseAccessMixin, ListView):
     
    model = Tutoria
    template_name='Tutorias/historialtutoria.html'

    def get_queryset(self) -> QuerySet[Any]:
        
        if Tutor.objects.filter(pk=self.request.user.pk).exists():
            # Tutorias correspondientes al tutor
            queryset = super().get_queryset().filter(tutor=self.request.user.pk)
        else: 
            # Tutorias correspondientes al alumno
            queryset = super().get_queryset().filter(alumno=self.request.user)
        
        if self.request.user.is_superuser == 1: 
            # Muestra todas las tutorias para el primer usuario creado (generalmente el primer superuser)
            queryset = super().get_queryset().all()
        
        return queryset




class VerTutoriasCordinadorListView(CordinadorViewMixin, ListView):
     
    model = Tutoria
    template_name='Tutorias/verTutorias_cordinador.html'

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset().all()   
        
        return queryset 


class VerTutoriasCodaListView(CodaViewMixin, ListView):
     
    model = Tutoria
    template_name='Tutorias/verTutorias_cooda.html'
    

    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset().filter(tutor=self.kwargs.get('pk'))   
        
        return queryset 
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tutor = Tutor.objects.get(pk=self.kwargs.get('pk'))
        context["tutor"] = tutor
        return context

class VerTutoresListView(CodaViewMixin, ListView):
    model = Tutor
    template_name = 'Tutorias/verTutores_coda.html'
    
class VerTutoradosCodaListView(CodaViewMixin, ListView):
    model = Alumno
    template_name = 'Tutorias/verTutorados_coda.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        
        queryset = super().get_queryset().filter(tutor_asignado=self.kwargs.get('pk'))   
        
        return queryset 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tutor = Tutor.objects.get(pk=self.kwargs.get('pk'))
        context["tutor"] = tutor
        return context

class VerTutoriasTutorListView(TutorViewMixin, ListView):
     
    model = Tutoria
    template_name='Tutorias/verTutorias_tutor.html'

    def get_queryset(self) -> QuerySet[Any]:
        
        # Tutorias correspondientes al tutor
        queryset = super().get_queryset().filter(tutor=self.request.user)
    
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tutorados = Alumno.objects.filter(tutor_asignado=self.request.user)
        context["tutorados"] = [alumno for alumno in tutorados]
        return context


class VerTutoriasAlumnoListView(AlumnoViewMixin, ListView):
     
    model = Tutoria
    template_name='Tutorias/verTutorias_alumno.html'

    def get_queryset(self) -> QuerySet[Any]:
        
        # Tutorias correspondientes al alumno
        
        queryset = super().get_queryset().filter(alumno=self.request.user)
        #if self.request.user.is_superuser == 1: 
            # Muestra todas las tutorias para el primer usuario creado (generalmente el primer superuser)
            #queryset = super().get_queryset().all()
        
        return queryset
    

# TODO Eliminar para prod
# class DebugTutoriasView(LoginRequiredMixin, ListView):

#     model = Tutoria
#     template_name='Tutorias/verTutorias_coordinador.html'

#     def get_queryset(self) -> QuerySet[Any]:
#         return super().get_queryset()
    
    
class QuickCreateTutoriaView(AlumnoViewMixin, CreateView):
    model = Tutoria
    template_name = 'Tutorias/registrar-tutoria.html'
    success_url = reverse_lazy('login_success')

    form_class = FormTutorias

    def form_valid(self, form: FormTutorias) -> HttpResponse:
        alumno = get_object_or_404(Alumno, pk=self.request.user)
        form.instance.alumno = alumno
        form.instance.tutor = alumno.tutor_asignado
        form.instance.estado = ACEPTADO
        
        
        rol = self.request.user.get_rol()
        if rol == ALUMNO:
            recipient = alumno.tutor_asignado   # No sé que hace este bloque, pero no lo voy a quitar para que no se rompa. -Alfredo
        else:
            recipient = Alumno.objects.filter(pk=self.get_object().alumno)
        
        notify.send(alumno, recipient=recipient, verb='Tutoria registrada con QR')

        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print("Tutoria invalida")
        print(f'Form: {form.instance}')
        return super().form_invalid(form)

    def get_initial(self) -> dict[str, Any]:
        super().get_initial()
        try:
            alumno = Alumno.objects.get(pk=self.request.user.pk)
        except Alumno.DoesNotExist:
            raise PermissionDenied("Sólo los alumnos pueden registrar tutorias con QR")
        self.initial["alumno"] = alumno
        self.initial["tutor"] = alumno.tutor_asignado
        self.initial["tema"] = alumno.tutor_asignado.tema_tutorias
        print(f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        self.initial["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.initial["descripcion"] = "Tutoria registrada con QR"
        return self.initial 
      
    
class VerTutoradosTutorListView(TutorViewMixin, ListView):
     
    model = Alumno
    template_name='Tutorias/list_tutorados.html'

    def get_queryset(self) -> QuerySet[Any]:
        
        # Tutorias correspondientes al tutor
        queryset = super().get_queryset().filter(tutor_asignado=self.request.user)
    
        return queryset

# Este es para asesorias, aun no se va a usar
class QRCodeView(View):
    def get(self, request):
        # Obtengo el usuario
        user_id = request.user.id

        # Creo qr
        qr_content = f"User ID: {user_id}"

        # Crea el qr
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)


        img = qr.make_image(fill_color="black", back_color="white")

        # Mando htttppp
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")

        return response


class CrearTutoriaPorAlumnoView(TutorViewMixin, CreateView):
    model = Tutoria
    form_class = FormTutorias
    template_name = 'Tutorias/solicitudTutoria.html'
    success_url = reverse_lazy('login_success')  # Cambia esto a la URL adecuada

    def form_valid(self, form):
        # Obtén el nombre del alumno desde la URL
        alumno_pk = self.kwargs.get('pk_alumno')

        # Busca el alumno por nombre
        alumno = get_object_or_404(Alumno, pk=alumno_pk)

        # Completa el formulario con los datos del alumno
        form.instance.alumno = alumno
        form.instance.tutor = alumno.tutor_asignado

        # Genera un slug único para la tutoría (puedes ajustar esto según tus necesidades)
        slug = slugify(form.instance.tema)
        form.instance.slug = slug

        return super().form_valid(form)
