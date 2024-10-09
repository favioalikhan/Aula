# views.py
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    EmprendedorForm,
    MentorForm,
    SolicitudMentoriaForm,
    CustomAuthenticationForm,
)
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from programa_startup.models import IntegranteStartup, Startup
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from .models import Mentor, Mentoria, SeguidorStartup, CustomUser
from programa_startup.models import Notificacion
import sendgrid
from sendgrid.helpers.mail import Content, To, Email, Mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate

# Create your views here.


class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get("remember_me"):
            # Set the session expiry to 30 days (or any duration you prefer)
            self.request.session.set_expiry(30 * 24 * 60 * 60)
        else:
            # Set session to expire when the browser is closed
            self.request.session.set_expiry(0)
        return response


def send_password_reset_email(email, context):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email(
        "favio_alikhan30@hotmail.com"
    )  # Cambia esto por el correo verificado
    to_email = To(email)
    subject = "Restablecimiento de Contraseña"
    content = Content("text/html", context["email_body"])

    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.send(mail)
        print(f"SendGrid response status code: {response.status_code}")
        print(f"SendGrid response body: {response.body}")
        print(f"SendGrid response headers: {response.headers}")
        return response
    except Exception as e:
        print(e.message)
        return None


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = CustomUser.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Restablecimiento de Contraseña"
                    email_template_name = "usuarios/password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": get_current_site(request).domain,
                        "site_name": "Aula Incuval",
                        "subject": subject,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    }
                    email_body = render_to_string(email_template_name, c)
                    context = {"email_body": email_body}
                    send_password_reset_email(user.email, context)
                messages.success(
                    request,
                    "Se ha enviado un correo con instrucciones para restablecer la contraseña.",
                )
                return redirect("password-reset-done")
            else:
                messages.error(
                    request, "No hay usuarios asociados con esta dirección de correo."
                )
    else:
        form = PasswordResetForm()
    return render(request, "usuarios/password_reset_form.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Autenticar al usuario recién creado
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            authenticated_user = authenticate(email=email, password=raw_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, "Registro exitoso. Bienvenido!")
                return redirect("/")  # Asume que tienes una vista 'home'
            else:
                messages.error(
                    request, "No se pudo autenticar al usuario después del registro."
                )
        else:
            messages.error(
                request, "Hubo un error en el registro. Por favor, revisa los datos."
            )
    else:
        form = CustomUserCreationForm()

    return render(request, "usuarios/register.html", {"form": form})


def get_success_url(self):
    return self.request.POST.get("next", "/")


"""
   La función `profile` verifica si un usuario tiene un perfil de emprendedor o mentor y
recupera información relevante para mostrar en la página de perfil del usuario.

:param request: El fragmento de código que proporcionó es una función de visualización en Django que maneja la página de perfil
de un usuario. Verifica si el usuario tiene un perfil de emprendedor o mentor y luego
prepara los datos de contexto en consecuencia para representar la información del perfil en la plantilla
'profile_user.html'
:return: La función `profile()` está devolviendo una plantilla representada 'usuarios/profile_user.html' con
un diccionario de contexto que contiene información basada en el tipo de perfil del usuario. El diccionario de contexto
incluye diferentes datos según si el usuario tiene un "emprendedor_profile", un
"mentor_profile" o ninguno. 
"""


@login_required
def profile(request):
    user = request.user

    # Verificar si el usuario tiene un perfil de emprendedor
    if hasattr(user, "emprendedor_profile"):
        emprendedor_profile = user.emprendedor_profile
        # Procesar los campos que contienen listas
        sectores_interes = (
            emprendedor_profile.sectores_interes.split(",")
            if emprendedor_profile.sectores_interes
            else []
        )
        habilidades_blandas = (
            emprendedor_profile.habilidades_blandas.split(",")
            if emprendedor_profile.habilidades_blandas
            else []
        )

        # Obtener las startups seguidas
        startups_seguidas = SeguidorStartup.objects.filter(
            usuario=emprendedor_profile
        ).select_related("startup")

        context = {
            "profile_type": "emprendedor",
            "sectores_interes": sectores_interes,
            "habilidades_blandas": habilidades_blandas,
            "startups_seguidas": startups_seguidas,
        }

    # Verificar si el usuario tiene un perfil de mentor
    elif hasattr(user, "mentor_profile"):
        mentor_profile = user.mentor_profile
        mentoria_startups = Mentoria.objects.filter(mentor=mentor_profile)

        context = {
            "profile_type": "mentor",
            "mentoria_startups": mentoria_startups,
            "mentor_profile": mentor_profile,
        }

    else:
        # Si no tiene ni perfil de emprendedor ni de mentor, puedes manejar este caso
        context = {
            "profile_type": "unknown",
        }

    return render(request, "usuarios/profile_user.html", context)


# La clase `EditProfile` maneja la edición de perfiles de usuario, incluyendo formularios para
# diferentes tipos de perfiles como 'emprendedor' y 'mentor'..
class EditProfile(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/edit_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_form"] = CustomUserChangeForm(instance=user)

        # Cambiar esto
        if hasattr(user, "emprendedor_profile"):
            context["emprendedor_form"] = EmprendedorForm(
                instance=user.emprendedor_profile
            )
            # Obtener las startups seguidas por el emprendedor
            startups_seguidas = SeguidorStartup.objects.filter(
                usuario=user.emprendedor_profile
            ).select_related("startup")
            context["startups_seguidas"] = startups_seguidas
        else:
            context["emprendedor_form"] = EmprendedorForm()

        # Verificar si el usuario tiene un perfil de mentor
        if hasattr(user, "mentor_profile"):
            context["mentor_form"] = MentorForm(instance=user.mentor_profile)
            mentoria_startups = Mentoria.objects.filter(mentor=user.mentor_profile)
            context["mentoria_startups"] = mentoria_startups
        else:
            context["mentor_form"] = MentorForm()

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=user)

        # Cambiar esto también
        if hasattr(user, "emprendedor_profile"):
            emprendedor_form = EmprendedorForm(
                request.POST, request.FILES, instance=user.emprendedor_profile
            )
        else:
            emprendedor_form = EmprendedorForm(request.POST, request.FILES)

        if hasattr(user, "mentor_profile"):
            mentor_form = MentorForm(
                request.POST, request.FILES, instance=user.mentor_profile
            )
        else:
            mentor_form = MentorForm(request.POST, request.FILES)

        if user_form.is_valid() and (
            emprendedor_form.is_valid() or mentor_form.is_valid()
        ):
            user_form.save()
            if hasattr(user, "emprendedor_profile"):
                emprendedor_form.save()
            if hasattr(user, "mentor_profile"):
                mentor_form.save()

            messages.success(request, "Perfil actualizado con éxito.")
            return redirect(reverse("profile"))
        else:
            messages.error(request, "El perfil no se pudo actualizar.")

        context = self.get_context_data()
        context["user_form"] = user_form
        context["emprendedor_form"] = emprendedor_form
        context["mentor_form"] = mentor_form
        return render(request, "usuarios/edit_profile.html", context)


# eliminar usuario
@login_required
def delete_account(request):
    user = request.user

    # Check if the user is the founder of a startup
    startup = Startup.objects.filter(fundador=user).first()
    if startup:
        # Delete all the members of the startup
        IntegranteStartup.objects.filter(startup=startup).delete()
        # Delete the startup
        startup.delete()

    # Delete the user
    user.delete()

    # Logout the user
    logout(request)

    # Redirect the user to the login page or any other desired page
    return redirect("login")


# Solicitar mentoria
@method_decorator(login_required, name="dispatch")
class SolicitarMentoriaView(CreateView):
    model = Mentoria
    form_class = SolicitudMentoriaForm
    template_name = "programa_startup/solicitar_mentoria.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["startup"] = self.get_startup()
        return kwargs

    def get_startup(self):
        return get_object_or_404(Startup, fundador=self.request.user)

    def form_valid(self, form):
        form.instance.startup = self.get_startup()
        form.instance.estado = "Pendiente"
        mentor_id = self.kwargs.get("mentor_id")
        mentor = get_object_or_404(Mentor, id=mentor_id)
        form.instance.mentor = mentor
        # Notificación al mentor sobre la nueva solicitud de mentoría

        if mentor.user:
            # Notificación al mentor sobre la nueva solicitud de mentoría
            Notificacion.objects.create(
                usuario=mentor.user,  # Usa mentor.user en lugar de form.instance.mentor
                tipo="Mentoria",
                mensaje=f"Tienes una nueva solicitud de mentoría de la startup '{form.instance.startup.nombre}'.",
            )
        else:
            print(f"Error: El mentor con ID {mentor_id} no tiene un usuario asociado.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentor_id = self.kwargs.get("mentor_id")
        context["mentor"] = get_object_or_404(Mentor, id=mentor_id)
        return context

    def get_success_url(self):
        return reverse(
            "listar-todos"
        )  # Cambia 'profile-startup' por la URL correcta si es necesario


@login_required
@require_POST
def cancelar_mentoria(request, mentoria_id):
    try:
        # Verificar que el usuario tenga un perfil de emprendedor y una startup asociada
        emprendedor_profile = getattr(request.user, "emprendedor_profile", None)
        if not emprendedor_profile or not emprendedor_profile.startup:
            return JsonResponse(
                {"status": "error", "message": "No tienes una startup asociada."},
                status=403,
            )

        startup = emprendedor_profile.startup

        # Buscar la mentoría asociada a la startup del usuario
        mentoria = Mentoria.objects.select_related("startup", "mentor").get(
            pk=mentoria_id, startup=startup
        )

        # Verificar que el usuario sea el fundador de la startup
        if mentoria.startup.fundador == request.user:
            with transaction.atomic():
                # Crear notificación para el mentor
                Notificacion.objects.create(
                    usuario=mentoria.mentor.user,
                    tipo="Mentoria",
                    mensaje=f"La mentoría con la startup '{mentoria.startup.nombre}' ha sido cancelada.",
                )

                # Eliminar la mentoría
                mentoria.delete()

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No tienes permiso para cancelar esta mentoría",
                },
                status=403,
            )
    except Mentoria.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Mentoría no encontrada"}, status=404
        )
    except AttributeError:
        return JsonResponse(
            {"status": "error", "message": "Usuario no autorizado o perfil incompleto"},
            status=403,
        )


def marcar_mentoria_completada(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mentoria_id = data.get("mentoria_id")

        try:
            # Iniciar una transacción atómica
            with transaction.atomic():
                # Buscar la mentoría asociada al mentor actual
                mentoria = Mentoria.objects.get(
                    id=mentoria_id, mentor=request.user.mentor_profile
                )

                # Marcar la mentoría como completada
                mentoria.estado = "COMPLETADA"
                mentoria.save()

                # Crear notificación para el fundador de la startup
                Notificacion.objects.create(
                    usuario=mentoria.startup.fundador,
                    tipo="Mentoria",
                    mensaje=f"La mentoría con el mentor '{mentoria.mentor.user.username}' ha sido marcada como completada.",
                )

            return JsonResponse({"success": True})
        except Mentoria.DoesNotExist:
            return JsonResponse({"success": False, "error": "Mentoría no encontrada."})


# notificaciones
"""
def crear_notificacion(usuario, tipo, mensaje):
    Notificacion.objects.create(
        usuario=usuario,
        tipo=tipo,
        mensaje=mensaje,
        fecha_creacion=timezone.now()
    )
    
@login_required
def mostrar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    # Verifica si hay notificaciones no leídas
    notificaciones_no_leidas = notificaciones.filter(leido=False).exists()

    return render(request, 'programa_startup/notificaciones.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    })

#notificaciones v2.0
def notificar_entregable(usuario, tarea):
    # Obtener todos los usuarios de la startup
    integrantes = Emprendedor.objects.filter(startup=usuario.emprendedor_profile.startup).values_list('user', flat=True)
    
    for integrante in integrantes:
        # Crear un mensaje de notificación
        mensaje = f"{usuario.username} ha subido el entregable para la tarea: {tarea.titulo}."
        
        # Crear una nueva notificación en la base de datos
        Notificacion.objects.create(usuario=integrante, tipo='Tarea', mensaje=mensaje)
        
@login_required
def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'programa_startup/notificaciones.html', {'notificaciones': notificaciones})
"""


@login_required
def ruta_emprendedor(request):
    # Obtener la startup del emprendedor
    startup = request.user.emprendedor_profile.startup

    # Verificar si la startup está inscrita en un programa
    if not startup or not startup.programa:
        return redirect("profile-startup")  # Redirigir si no tiene startup o programa

    context = {
        "startup": startup,
        "programa": startup.programa,
    }

    return render(request, "usuarios/ruta_emprendedor.html", context)
