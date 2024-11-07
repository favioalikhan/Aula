from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import (
    Evento,
    Notificacion,
    ProgramaPage,
    Startup,
    IntegranteStartup,
    Tarea,
    Entregable,
    Modulo,
    Sprint,
    Logro,
)
from django.http import JsonResponse
from usuarios.models import CustomUser, Emprendedor, Mentor, Mentoria, SeguidorStartup
from django.db.models import OuterRef, Exists, Subquery, Q
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# ---------Crear sesiones y tareas------------------
from .models import Sesion
from django.views.generic import DetailView
from .forms import (
    CalificacionForm,
    SesionForm,
    TareaForm,
    StartupForm,
    EntregableForm,
    LogroForm,
)
from wagtail.models import Page
from django.views import View
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


"""
    Esta función se utiliza para inscribir una startup en un programa, con comprobaciones de validación de
permisos de usuario y asociación de startup existente.

:param request: El parámetro `request` en la función `inscribir_startup` es un objeto HttpRequest
que representa la solicitud HTTP actual. Contiene información sobre la solicitud realizada por el
usuario, como el usuario que realiza la solicitud, el método utilizado (GET, POST, etc.) y cualquier dato enviado con
el
:param programa_id: El parámetro `programa_id` en la función `inscribir_startup` representa el
identificador único del programa en el que se está inscribiendo o registrando una startup. Este parámetro
se utiliza para recuperar el programa específico de la base de datos en función de su ID para que la startup pueda
inscribirse en ese programa en particular
:return: La función `inscribir_startup` está devolviendo una respuesta de redirección a la vista denominada
`programa-modulo` con el parámetro slug establecido en `programa.slug`. Esta redirección se realiza después de
inscribir con éxito un inicio en un programa. Si el inicio ya está inscrito en el programa,
se muestra un mensaje de advertencia y se realiza la misma redirección sin realizar ningún cambio.
"""


@login_required
def inscribir_startup(request, programa_id):
    programa = get_object_or_404(ProgramaPage, id=programa_id)
    emprendedor_profile = getattr(request.user, "emprendedor_profile", None)

    if not emprendedor_profile or emprendedor_profile.cargo != "Founder":
        raise PermissionDenied(
            "Solo los fundadores pueden inscribir startups en un programa."
        )

    startup = emprendedor_profile.startup
    if not startup:
        raise PermissionDenied(
            "No se encontró ninguna startup asociada a este usuario."
        )

    if startup.programa == programa:
        messages.warning(request, "Esta startup ya está inscrita en este programa.")
        return redirect("programa-modulo", slug=programa.slug)

    # Asignar el programa a la startup y establecer la fecha de inscripción
    startup.programa = programa
    startup.fecha_inscripcion = timezone.now()
    startup.save()

    messages.success(request, "Startup inscrita exitosamente en el programa.")
    return redirect("programa-modulo", slug=programa.slug)


# crear startup
@login_required
def crear_startup(request):
    # Verifica que el usuario no tenga una startup asociada
    if (
        hasattr(request.user, "emprendedor_profile")
        and request.user.emprendedor_profile.startup
    ):
        messages.warning(request, "Ya tienes una startup asociada.")
        return redirect("profile")  # Redirige a la página de perfil del usuario

    if request.method == "POST":
        form = StartupForm(request.POST, request.FILES)
        if form.is_valid():
            startup = form.save(commit=False)
            startup.fundador = request.user
            startup.save()

            # Asocia la startup al perfil del emprendedor
            emprendedor_profile = request.user.emprendedor_profile
            emprendedor_profile.startup = startup
            emprendedor_profile.save()

            # Procesar integrantes enviados en el formulario
            integrantes = request.POST.getlist(
                "integrantes"
            )  # Lista de strings "user_id:cargo"
            for integrante in integrantes:
                try:
                    user_id, cargo = integrante.split(":", 1)
                    usuario = get_object_or_404(CustomUser, id=user_id)

                    # Verificar que el usuario aún no es integrante de otra startup
                    if IntegranteStartup.objects.filter(usuario=usuario).exists():
                        continue  # O manejar según sea necesario

                    # Agregar al usuario como integrante
                    integrante_startup = IntegranteStartup.objects.create(
                        usuario=usuario,
                        startup=startup,
                        cargo=cargo,
                        agregado_por=request.user,
                    )

                    if hasattr(usuario, "emprendedor_profile"):
                        usuario.emprendedor_profile.startup = startup
                        usuario.emprendedor_profile.save()

                    # Notificar al integrante sobre su inclusión en la startup
                    mensaje = f"Has sido agregado como '{integrante_startup.cargo}' a la startup '{startup.nombre}' por {request.user.username}."
                    Notificacion.objects.create(
                        usuario=usuario, tipo="Equipo", mensaje=mensaje
                    )

                except ValueError:
                    # Manejar el caso donde el formato no es "user_id:cargo"
                    continue

            # Notificar al fundador de la creación exitosa de la startup
            Notificacion.objects.create(
                usuario=request.user,
                tipo="Startup",
                mensaje=f"Has creado la startup '{startup.nombre}'.",
            )

            messages.success(request, "Startup creada exitosamente.")
            return redirect("profile-startup")
    else:
        form = StartupForm()

    return render(request, "programa_startup/register_startup.html", {"form": form})


class EditProfileStartup(LoginRequiredMixin, TemplateView):
    template_name = "programa_startup/edit_startup.html"

    def get_startup(self):
        user = self.request.user
        try:
            return Startup.objects.get(fundador=user)
        except Startup.DoesNotExist:
            integrante = IntegranteStartup.objects.filter(usuario=user).first()
            return integrante.startup if integrante else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startup = self.get_startup()

        if not startup:
            messages.error(self.request, "No tienes acceso a ninguna startup.")
            return context

        integrantes = IntegranteStartup.objects.filter(startup=startup)

        mentorias = startup.mentoria_set.all()

        context.update(
            {
                "startup": startup,
                "integrantes": integrantes,
                "seguidores_count": startup.seguidores_startup.count(),
                "progreso": round(startup.progreso),
                "hitos_count": startup.logros.count(),
                "startup_form": StartupForm(instance=startup),
                "logro_form": LogroForm(),
                "mentorias": mentorias,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        startup = self.get_startup()
        if not startup:
            return redirect("profile")

        with transaction.atomic():
            # Actualizar información de la startup
            startup_form = StartupForm(request.POST, request.FILES, instance=startup)
            if startup_form.is_valid():
                startups = startup_form.save(commit=False)
                startups.save()
                # Procesar logros existentes
                logro_ids = request.POST.getlist("logro_ids")
                for logro_id in logro_ids:
                    logro = Logro.objects.get(id=logro_id)
                    if request.POST.get(f"eliminar_logro_{logro_id}"):
                        logro.delete()
                    else:
                        logro.titulo = request.POST.get(f"logro_titulo_{logro_id}")
                        logro.descripcion = request.POST.get(
                            f"logro_descripcion_{logro_id}"
                        )
                        logro.fecha_logro = request.POST.get(
                            f"logro_fecha_logro_{logro_id}"
                        )
                        logro.save()

                # Procesar nuevos logros
                nuevo_logro_titulos = request.POST.getlist("nuevo_titulo")
                nuevo_logro_descripciones = request.POST.getlist("nueva_descripcion")
                nuevo_logro_fechas = request.POST.getlist("nueva_fecha_logro")

                for i in range(len(nuevo_logro_titulos)):
                    if nuevo_logro_titulos[i]:  # Verifica que el título no esté vacío
                        Logro.objects.create(
                            startup=startup,
                            titulo=nuevo_logro_titulos[i],
                            descripcion=nuevo_logro_descripciones[i],
                            fecha_logro=nuevo_logro_fechas[i],
                        )

                messages.success(request, "Perfil de la startup actualizado con éxito.")
            else:
                messages.error(
                    request, "No se pudo actualizar el perfil de la startup."
                )
                return self.get(request, *args, **kwargs)

            # Procesar nuevos integrantes
            nuevos_integrantes = request.POST.getlist("integrantes")
            for nuevo_integrante in nuevos_integrantes:
                user_id, cargo = nuevo_integrante.split(":", 1)
                usuario = CustomUser.objects.get(id=user_id)

                # Verificar si el usuario ya es integrante de esta startup
                if not IntegranteStartup.objects.filter(
                    startup=startup, usuario=usuario
                ).exists():
                    # Verificar si el usuario es integrante de otra startup
                    if IntegranteStartup.objects.filter(usuario=usuario).exists():
                        messages.warning(
                            request,
                            f"{usuario.username} ya es integrante de otra startup.",
                        )
                        continue

                    IntegranteStartup.objects.create(
                        startup=startup,
                        usuario=usuario,
                        cargo=cargo,
                        agregado_por=request.user,
                    )

                    if hasattr(usuario, "emprendedor_profile"):
                        usuario.emprendedor_profile.startup = startup
                        usuario.emprendedor_profile.save()

            # Procesar edición de mentorías
            mentoria_ids = request.POST.getlist("mentoria_id")
            for mentoria_id in mentoria_ids:
                try:
                    mentoria = Mentoria.objects.get(id=mentoria_id, startup=startup)
                    # Actualizar los campos directamente
                    mentoria.temas = request.POST.get(f"mentoria_temas_{mentoria_id}")
                    mentoria.fecha = request.POST.get(f"mentoria_fecha_{mentoria_id}")
                    mentoria.save()
                except Mentoria.DoesNotExist:
                    messages.warning(
                        request,
                        f"La mentoría con ID {mentoria_id} no existe o no pertenece a esta startup.",
                    )
        return redirect(reverse("profile-startup"))


@login_required
@require_POST
def eliminar_integrante(request, integrante_id):
    try:
        integrante = IntegranteStartup.objects.get(pk=integrante_id)
        if (
            integrante.startup.fundador == request.user
            and integrante.usuario != request.user
        ):
            with transaction.atomic():
                # Eliminar la asociación del usuario con la startup
                if hasattr(integrante.usuario, "emprendedor_profile"):
                    integrante.usuario.emprendedor_profile.startup = None
                    integrante.usuario.emprendedor_profile.save()

                integrante.delete()

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No tienes permiso para eliminar este integrante",
                },
                status=403,
            )
    except IntegranteStartup.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Integrante no encontrado"}, status=404
        )


def eliminar_startup(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    if request.method == "POST":
        if (
            request.user.rol == request.user.EMPRENDEDOR
            and request.user.emprendedor_profile.cargo == "Founder"
        ):
            startup.delete()
            messages.success(request, "La startup ha sido eliminada exitosamente.")
            return redirect(reverse("profile"))
        else:
            messages.error(request, "No tienes permiso para eliminar esta startup.")
            return redirect(reverse("profile-startup"))
    return redirect(reverse("profile-startup"))


@login_required
def salir_startup(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    user_profile = request.user.emprendedor_profile

    # Buscar si el usuario es un integrante de la startup
    integrante = IntegranteStartup.objects.filter(
        startup=startup, usuario=request.user
    ).first()

    if integrante:
        # Eliminar la relación entre el usuario y la startup
        integrante.delete()

        # Desasociar el usuario de la startup en su perfil de emprendedor
        user_profile.startup = None
        user_profile.save()

        messages.success(request, "Has salido de la startup exitosamente.")
    else:
        messages.error(request, "No perteneces a esta startup.")

    return redirect("profile")  # Redirigir al perfil del usuario


"""
Funciona
Para filtrar solo emprendedores
@require_GET
def search_integrante(request):
    query = request.GET.get('query', '')
    
    # Subconsulta para verificar si el usuario está asociado a alguna startup
    if query:
        # Filtrar usuarios cuyo username contiene 'query' y cuyo rol es 'Emprendedor'
        # results = CustomUser.objects.filter(username__icontains=query, rol='emprendedor') #funciona
        results = CustomUser.objects.filter(username__icontains=query, rol='emprendedor')
        # Preparar la respuesta en un formato adecuado
        integrantes = [{'id': u.id, 'nombre': f"{u.username}"} for u in results]
    else:
        integrantes = []

    return JsonResponse({'results': integrantes})
"""

"""
Funciona
Para filtrar solo emprendedores que no tengan startup pero existe redundancia
@require_GET
def search_integrante(request):
    query = request.GET.get('query', '')

    if query:
        # Filtrar usuarios cuyo username contiene 'query' y cuyo rol es 'Emprendedor'
        results = CustomUser.objects.filter(
            username__icontains=query,
            rol='emprendedor'
        ).filter(
            # Excluir aquellos emprendedores que ya están asociados a una startup
            Q(emprendedor_profile__startup__isnull=True)
        )

        # Preparar la respuesta en un formato adecuado
        integrantes = [{'id': u.id, 'nombre': f"{u.username}"} for u in results]
    else:
        integrantes = []

    return JsonResponse({'results': integrantes})
"""


# Funciona: Para filtrar solo emprendedores que no tengan startup de forma precisa usando exists
@require_GET
def search_integrante(request):
    query = request.GET.get("query", "")

    # Subconsulta para verificar si el emprendedor está asociado a una startup
    startup_association = Emprendedor.objects.filter(
        user=OuterRef("pk"), startup__isnull=False
    )

    if query:
        # Filtrar usuarios cuyo username contiene 'query' y cuyo rol es 'Emprendedor'
        results = (
            CustomUser.objects.filter(username__icontains=query, rol="emprendedor")
            .annotate(is_associated=Exists(startup_association))
            .filter(is_associated=False)
        )

        # Preparar la respuesta en un formato adecuado
        integrantes = [{"id": u.id, "nombre": f"{u.username}"} for u in results]
    else:
        integrantes = []

    return JsonResponse({"results": integrantes})


# agregar integrante
@require_POST
def agregar_integrante(request):
    usuario_id = request.POST.get("usuario_id")
    cargo = request.POST.get("cargo")
    startup_id = request.POST.get("startup_id")

    usuario = get_object_or_404(CustomUser, id=usuario_id)
    startup = get_object_or_404(Startup, id=startup_id)

    # Verificar que el usuario tiene el rol de emprendedor antes de agregarlo
    if usuario.rol != "Emprendedor":
        return JsonResponse(
            {
                "status": "error",
                "message": "Solo los usuarios con el rol de Emprendedor pueden ser agregados.",
            }
        )

    # Crear el nuevo integrante
    IntegranteStartup.objects.create(
        usuario=usuario, startup=startup, cargo=cargo, agregado_por=request.user
    )

    return JsonResponse(
        {
            "status": "success",
            "message": f"{usuario.username} ha sido agregado como {cargo}.",
        }
    )


# mostrar perfil startup
@login_required
def profile_startup(request):
    # Buscar la startup donde el usuario es el fundador o un integrante
    startup = None

    try:
        # Primero, intenta obtener la startup donde el usuario es fundador
        startup = Startup.objects.get(fundador=request.user)
    except Startup.DoesNotExist:
        # Si no es fundador, busca si el usuario es un integrante de alguna startup
        integrante = IntegranteStartup.objects.filter(usuario=request.user).first()
        if integrante:
            startup = integrante.startup

    # Si no se encuentra ninguna startup, mostrar un mensaje de error y redirigir
    if not startup:
        messages.error(request, "No tienes acceso a ninguna startup.")
        return redirect("profile")  # Redirigir a la página de perfil del usuario

    # Obtener los integrantes de la startup
    integrantes = IntegranteStartup.objects.filter(startup=startup)

    # Obtener la cantidad de seguidores de la startup
    seguidores_count = startup.seguidores_startup.count()

    # Obtener el progreso de la startup
    progreso = round(startup.progreso)

    # Contar los hitos (logros) asociados a la startup
    hitos_count = startup.logros.count()

    # Obtener los logros asociados a la startup
    logros = startup.logros.all()

    context = {
        "startup": startup,
        "integrantes": integrantes,
        "seguidores_count": seguidores_count,
        "progreso": progreso,
        "hitos_count": hitos_count,
        "logros": logros,
    }
    return render(request, "programa_startup/profile_startup.html", context)


# -------------------------------------Crear sesiones y tareas---------------------------------------

"""
Esta función crea una sesión asociada con un sprint y redirecciona a una página de Wagtail
tras el envío exitoso del formulario.

:param request: El parámetro `request` en la función `crear_sesion` es un objeto HttpRequest que
representa la solicitud HTTP realizada por el usuario. Contiene información sobre la solicitud, como el
método de solicitud (GET, POST, etc.), datos de la sesión del usuario y cualquier dato enviado en la solicitud (datos del formulario
:param sprint_id: El parámetro `sprint_id` en la función `crear_sesion` se utiliza para identificar el
Sprint específico para el que se está creando una sesión. Se pasa como argumento a la función de vista
cuando un usuario accede a la URL asociada con esta vista. La función recupera el objeto Sprint
en función de esto.
:return: La función de vista `crear_sesion` devuelve una plantilla HTML renderizada llamada 'crear_sesion.html'
con los datos de contexto que contienen el formulario, el objeto de sprint y la URL del Página del módulo. Esta función de vista
maneja la creación de una sesión relacionada con un sprint específico y redirecciona a la página del módulo
después de guardar correctamente los datos del formulario de sesión.
"""


@login_required
def crear_sesion(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)

    if request.method == "POST":
        form = SesionForm(request.POST, request.FILES)
        if form.is_valid():
            sesion = form.save(commit=False)
            sesion.sprint = sprint
            sesion.save()

            # Redirigir al módulo usando la URL de Wagtail
            modulo_page = Page.objects.get(id=sprint.modulo.id)
            return redirect(modulo_page.get_url())
    else:
        form = SesionForm()

    # Obtener la URL del módulo para el enlace "Volver al módulo"
    modulo_page = Page.objects.get(id=sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    context = {"form": form, "sprint": sprint, "modulo_page_url": modulo_page_url}

    return render(request, "programa_startup/crear_sesion.html", context)


"""
Esta función crea una tarea asociada con una sesión y redirecciona a la página del módulo
tras la creación exitosa de la tarea.

:param request: El parámetro `request` en la función `crear_tarea` es un objeto HttpRequest que
representa la solicitud HTTP realizada por el usuario. Contiene información sobre la solicitud, como el
método de solicitud (GET, POST, etc.), datos del usuario y cualquier archivo cargado como parte de la solicitud. Este
:param sesion_id: El parámetro `sesion_id` en la función `crear_tarea` representa el identificador único
de una sesión. Esta función está diseñada para crear una nueva tarea asociada con una sesión específica identificada por `sesion_id`. El objeto de sesión se recupera utilizando `get_object_or_404` basado
en el
:return: La función de vista `crear_tarea` devuelve una plantilla HTML renderizada llamada 'crear_tarea.html'
junto con un diccionario de contexto que contiene las variables form, sesion, modulo_page_url y programa_slug. Esta plantilla se utiliza para crear una nueva tarea asociada con una sesión en un programa.
"""


@login_required
def crear_tarea(request, sesion_id):
    sesion = get_object_or_404(Sesion, pk=sesion_id)

    if request.method == "POST":
        form = TareaForm(request.POST, request.FILES)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.sesion = sesion
            tarea.save()

            # Obtener el programa y las startups asociadas
            programa_page = sesion.sprint.modulo.get_parent().specific
            if isinstance(programa_page, ProgramaPage):
                integrantes = IntegranteStartup.objects.filter(
                    startup__programa=programa_page
                ).select_related("usuario")

                # Crear notificación para cada integrante
                for integrante in integrantes:
                    mensaje = f"Nueva tarea asignada: {tarea.titulo} en la sesión {sesion.titulo}."
                    Notificacion.objects.create(
                        usuario=integrante.usuario, tipo="Tarea", mensaje=mensaje
                    )

                # Notificar al creador de la tarea
                Notificacion.objects.create(
                    usuario=request.user,
                    tipo="Tarea",
                    mensaje=f"Has creado la tarea '{tarea.titulo}' en la sesión '{sesion.titulo}'.",
                )

                messages.success(request, "Tarea creada exitosamente.")

            # Obtener la página del módulo
            modulo_page = Page.objects.get(id=sesion.sprint.modulo.id)
            return redirect(modulo_page.get_url())
    else:
        form = TareaForm()

    # Obtener la URL del módulo para el enlace "Volver al módulo"
    modulo_page = Page.objects.get(id=sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    # Obtener el slug del programa
    programa_page = sesion.sprint.modulo.get_parent().specific
    programa_slug = (
        programa_page.slug if isinstance(programa_page, ProgramaPage) else ""
    )

    context = {
        "form": form,
        "sesion": sesion,
        "modulo_page_url": modulo_page_url,
        "programa_slug": programa_slug,
    }

    return render(request, "programa_startup/crear_tarea.html", context)


@login_required
def ver_entregables(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    entregables = Entregable.objects.filter(tarea=tarea)

    # Obtener la página del módulo
    modulo_page = Page.objects.get(id=tarea.sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    context = {
        "tarea": tarea,
        "entregables": entregables,
        "modulo_page_url": modulo_page_url,
    }

    return render(request, "programa_startup/entregable.html", context)


"""
Esta función se utiliza para permitir que los speakers califiquen y revisen los entregables de un programa
de inicio.

:param request: El parámetro `request` en la función `calificar_resolucion` es un objeto HttpRequest
que representa la solicitud HTTP actual. Contiene información sobre la solicitud realizada por el cliente, como el método de solicitud (GET, POST, etc.), datos de la sesión del usuario y cualquier dato enviado en
la solicitud (
:param pk: El parámetro `pk` en la función `calificar_resolucion` representa la clave principal del objeto `Entregable` que se está procesando. Esta clave principal se utiliza para recuperar la instancia específica de `Entregable` de la base de datos utilizando la función `get_object_or_404`
:return: Se está devolviendo una función de vista llamada `calificar_resolucion`. Esta función es
responsable de manejar la lógica relacionada con la calibración de una resolución para una tarea en un programa de inicio. La función verifica si el usuario tiene el rol de 'orador' y, si no lo tiene, genera una
excepción PermissionDenied. Si el método de solicitud es POST, procesa los datos del formulario, actualiza el
estado de la resolución,
"""


@login_required
def calificar_resolucion(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)

    # Verificar que el usuario tenga el rol de mentor
    if not request.user.rol == "speaker":
        raise PermissionDenied("Solo los speakers pueden calificar entregables.")

    if request.method == "POST":
        form = CalificacionForm(request.POST, instance=entregable)
        if form.is_valid():
            entregable.estado = "revisado"
            form.save()
            return redirect("ver-entregables", tarea_id=entregable.tarea.pk)
    else:
        form = CalificacionForm(instance=entregable)

    context = {"form": form, "entregable": entregable}

    return render(request, "programa_startup/tarea_calificacion.html", context)


@login_required
def editar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)

    if request.method == "POST":
        form = SesionForm(request.POST, request.FILES, instance=sesion)
        if form.is_valid():
            form.save()

            # Obtener la página del módulo y redirigir
            modulo_page = Page.objects.get(id=sesion.sprint.modulo.id)
            return redirect(modulo_page.get_url())
    else:
        form = SesionForm(instance=sesion)

    # Obtener la URL del módulo para el enlace "Volver al módulo"
    modulo_page = Page.objects.get(id=sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    context = {"form": form, "sesion": sesion, "modulo_page_url": modulo_page_url}

    return render(request, "programa_startup/editar_sesion.html", context)


@login_required
def eliminar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)

    # Obtener la página del módulo antes de eliminar la sesión
    modulo_page = Page.objects.get(id=sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    if request.method == "POST":
        sesion.delete()
        return redirect(modulo_page_url)

    context = {"sesion": sesion, "modulo_page_url": modulo_page_url}
    return render(request, "programa_startup/eliminar_sesion.html", context)


@login_required
def editar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)

    if request.method == "POST":
        form = TareaForm(request.POST, request.FILES, instance=tarea)
        if form.is_valid():
            form.save()

            # Obtener el programa y las startups asociadas
            programa_page = tarea.sesion.sprint.modulo.get_parent().specific

            # Verificar que sea una instancia de ProgramaPage
            if isinstance(programa_page, ProgramaPage):
                integrantes = IntegranteStartup.objects.filter(
                    startup__programa=programa_page
                ).select_related("usuario")

                # Crear notificación para cada integrante
                for integrante in integrantes:
                    mensaje = f"La tarea '{tarea.titulo}' en la sesión '{tarea.sesion.titulo}' ha sido actualizada."
                    Notificacion.objects.create(
                        usuario=integrante.usuario, tipo="Tarea", mensaje=mensaje
                    )

                # Notificar al usuario que editó la tarea
                Notificacion.objects.create(
                    usuario=request.user,
                    tipo="Tarea",
                    mensaje=f"Has editado la tarea '{tarea.titulo}' en la sesión '{tarea.sesion.titulo}'.",
                )

                messages.success(request, "Tarea actualizada exitosamente.")

            # Obtener la página del módulo
            modulo_page = Page.objects.get(id=tarea.sesion.sprint.modulo.id)
            return redirect(modulo_page.get_url())
    else:
        form = TareaForm(instance=tarea)

    # Obtener la URL del módulo para el enlace "Volver al módulo"
    modulo_page = Page.objects.get(id=tarea.sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    # Obtener el slug del programa
    programa_page = tarea.sesion.sprint.modulo.get_parent().specific
    programa_slug = (
        programa_page.slug if isinstance(programa_page, ProgramaPage) else ""
    )

    context = {
        "form": form,
        "tarea": tarea,
        "modulo_page_url": modulo_page_url,
        "programa_slug": programa_slug,
    }

    return render(request, "programa_startup/editar_tarea.html", context)


@login_required
def eliminar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)

    # Obtener la página del módulo antes de eliminar la tarea
    modulo_page = Page.objects.get(id=tarea.sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    if request.method == "POST":
        tarea.delete()
        return redirect(modulo_page_url)

    context = {"tarea": tarea, "modulo_page_url": modulo_page_url}
    return render(request, "programa_startup/eliminar_tarea.html", context)


@method_decorator(login_required, name="dispatch")
class SubirEntregableView(View):
    def get(self, request, tarea_id):
        tarea = get_object_or_404(Tarea, pk=tarea_id)
        get_object_or_404(Startup, fundador=request.user)
        now = timezone.now()

        # Obtener la página del módulo
        modulo_page = Page.objects.get(id=tarea.sesion.sprint.modulo.id)
        modulo_page_url = modulo_page.get_url()

        entregable_existente = Entregable.objects.filter(
            tarea=tarea, subido_por=request.user
        ).first()

        form = EntregableForm(instance=entregable_existente)
        # Verificar si `fecha_entrega` es None
        can_upload = (
            (tarea.fecha_entrega is not None)
            and (now <= tarea.fecha_entrega)
            and (entregable_existente is None)
        )

        context = {
            "tarea": tarea,
            "form": form,
            "entregable": entregable_existente,
            "now": now,
            "modulo_page_url": modulo_page_url,
            "can_upload": can_upload,
        }
        return render(request, "programa_startup/subir_entregable.html", context)

    def post(self, request, tarea_id):
        tarea = get_object_or_404(Tarea, pk=tarea_id)
        startup = get_object_or_404(Startup, fundador=request.user)
        now = timezone.now()

        # Obtener la página del módulo
        modulo_page = Page.objects.get(id=tarea.sesion.sprint.modulo.id)
        modulo_page_url = modulo_page.get_url()

        entregable_existente = Entregable.objects.filter(
            tarea=tarea, subido_por=request.user
        ).first()

        form = EntregableForm(
            request.POST, request.FILES, instance=entregable_existente
        )

        if form.is_valid():
            entregable = form.save(commit=False)
            entregable.tarea = tarea
            entregable.subido_por = request.user
            entregable.startup = startup
            entregable.estado = "enviado"  # O el estado que consideres adecuado
            entregable.save()

            # Obtener todos los integrantes de la startup, incluyendo al fundador
            integrantes = list(startup.integrantes.all())
            integrantes.append(startup.fundador)

            # Crear notificaciones para todos los integrantes
            for integrante in integrantes:
                # No crear notificación para quien subió el entregable
                if integrante != request.user:
                    mensaje = (
                        f"La startup {startup.nombre} ha entregado la tarea '{tarea.titulo}' "
                        f"en la sesión '{tarea.sesion.titulo}' del módulo '{tarea.sesion.sprint.modulo.title}'."
                    )
                    Notificacion.objects.create(
                        usuario=integrante, tipo="Entregable", mensaje=mensaje
                    )

            # Notificación para quien subió el entregable
            Notificacion.objects.create(
                usuario=request.user,
                tipo="Entregable",
                mensaje=f"Has subido exitosamente el entregable para la tarea '{tarea.titulo}'.",
            )

            messages.success(request, "Entregable subido exitosamente.")
            return redirect(modulo_page_url)

        context = {
            "tarea": tarea,
            "form": form,
            "entregable": entregable_existente,
            "now": now,
            "modulo_page_url": modulo_page_url,
            "can_upload": (tarea.fecha_entrega is not None)
            and (now <= tarea.fecha_entrega)
            and (entregable_existente is None),
        }
        return render(request, "programa_startup/subir_entregable.html", context)


@login_required
def borrar_entregable(request, pk):
    entregable = get_object_or_404(Entregable, pk=pk)

    # Verificar si el usuario es el dueño del entregable
    if entregable.startup.fundador != request.user:
        return redirect("/")  # Redirige a la página principal si no tiene permiso

    if request.method == "POST":
        # Obtener la página del módulo antes de eliminar el entregable
        modulo_page = Page.objects.get(id=entregable.tarea.sesion.sprint.modulo.id)
        modulo_page_url = modulo_page.get_url()

        entregable.delete()

        return redirect(modulo_page_url)  # Redirige a la URL del módulo

    # Si no es una solicitud POST, redirige a la página del módulo
    modulo_page = Page.objects.get(id=entregable.tarea.sesion.sprint.modulo.id)
    modulo_page_url = modulo_page.get_url()

    return redirect(modulo_page_url)


# @login_required
def eventos_view(request):
    eventos = Evento.objects.live().order_by("fecha")

    if request.user.is_authenticated:
        # Filtrar las notificaciones no leídas de eventos para el usuario autenticado
        notificaciones_eventos = Notificacion.objects.filter(
            usuario=request.user, tipo="Evento", leido=False
        )
    else:
        # Para usuarios no autenticados, no hay notificaciones
        notificaciones_eventos = []

    return render(
        request,
        "programa_startup/lista_evento.html",
        {
            "events": eventos,
            "notificaciones_eventos": notificaciones_eventos,
        },
    )


class ProgramaModuloView(DetailView):
    model = ProgramaPage
    template_name = "programa_startup/programa_modulo.html"
    context_object_name = "programa"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener los módulos asociados al programa
        programa = self.get_object()
        context["modulos"] = Modulo.objects.filter(programa=programa)
        return context


# Listar objetos
def listar_todos(request):
    search_query = request.GET.get("search", "")
    page = request.GET.get("page", 1)
    tab = request.GET.get(
        "tab", "emprendedores"
    )  # Añadimos un parámetro para la pestaña activa

    # Filtrar según la pestaña activa
    if tab == "emprendedores":
        usuarios = Emprendedor.objects.select_related("user").order_by("user__username")
        if search_query:
            usuarios = usuarios.filter(
                Q(user__username__icontains=search_query)
                | Q(user__apellido_paterno__icontains=search_query)
                | Q(user__apellido_materno__icontains=search_query)
            )
        paginator = Paginator(usuarios, 6)
        try:
            usuarios_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            usuarios_page = paginator.page(1)
        context = {
            "usuarios": usuarios_page,
            "tab": tab,
            "search_query": search_query,
        }

    elif tab == "mentores":
        mentores = Mentor.objects.select_related("user").order_by("user__username")
        if search_query:
            mentores = mentores.filter(
                Q(user__username__icontains=search_query)
                | Q(user__apellido_paterno__icontains=search_query)
                | Q(user__apellido_materno__icontains=search_query)
            )
        paginator = Paginator(mentores, 6)
        try:
            mentores_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            mentores_page = paginator.page(1)
        context = {
            "mentores": mentores_page,
            "tab": tab,
            "search_query": search_query,
        }

    elif tab == "startups":
        startups = Startup.objects.select_related("fundador").order_by("nombre")
        if search_query:
            startups = startups.filter(
                Q(nombre__icontains=search_query)
                | Q(descripcion__icontains=search_query)
            )
        paginator = Paginator(startups, 6)
        try:
            startups_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            startups_page = paginator.page(1)
        context = {
            "startups": startups_page,
            "tab": tab,
            "search_query": search_query,
        }

    # Procesamiento adicional para usuarios autenticados
    emprendedor_profile = None
    seguidores_startup_ids = []

    if request.user.is_authenticated and hasattr(request.user, "emprendedor_profile"):
        emprendedor_profile = request.user.emprendedor_profile
        startup_profile = emprendedor_profile.startup

        seguidores_startup = SeguidorStartup.objects.filter(usuario=emprendedor_profile)
        seguidores_startup_ids = list(
            seguidores_startup.values_list("startup_id", flat=True)
        )

        seguimiento_subquery = SeguidorStartup.objects.filter(
            usuario=emprendedor_profile, startup=OuterRef("pk")
        ).values("id")

        if tab == "startups":
            startups_page.object_list = startups_page.object_list.annotate(
                seguimiento_id=Subquery(seguimiento_subquery[:1])
            )

        if startup_profile and tab == "mentores":
            mentorias_pendientes_subquery = Mentoria.objects.filter(
                startup=startup_profile, mentor=OuterRef("pk"), estado="Pendiente"
            )
            mentores_page.object_list = mentores_page.object_list.annotate(
                mentoria_pendiente_id=Subquery(
                    mentorias_pendientes_subquery.values("id")[:1]
                ),
                tiene_mentoria_pendiente=Exists(mentorias_pendientes_subquery),
            )

    context.update(
        {
            "emprendedor_profile": emprendedor_profile,
            "seguidores_startup_ids": seguidores_startup_ids,
            "search_query": search_query,
        }
    )

    # Comprobar si es una solicitud AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Renderizar el contenido de la pestaña activa y devolverlo como JSON
        if tab == "emprendedores":
            html = render_to_string(
                "partials/emprendedores_lista.html", context, request=request
            )
        elif tab == "mentores":
            html = render_to_string(
                "partials/mentores_lista.html", context, request=request
            )
        elif tab == "startups":
            html = render_to_string(
                "partials/startups_lista.html", context, request=request
            )
        else:
            html = ""

        return JsonResponse({"html": html})

    return render(request, "programa_startup/listar_todos.html", context)


@login_required
def seguir_startup(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    emprendedor_profile = request.user.emprendedor_profile
    if emprendedor_profile.startup and startup.id == emprendedor_profile.startup.id:
        messages.error(request, "No puedes seguir tu propia startup.")
        return redirect("listar-todos")
    if not SeguidorStartup.objects.filter(
        usuario=request.user.emprendedor_profile, startup=startup
    ).exists():
        SeguidorStartup.objects.create(
            usuario=request.user.emprendedor_profile, startup=startup
        )
    return redirect("listar-todos")


@login_required
@require_POST
def dejar_de_seguir_startup(request, seguimiento_id):
    try:
        # Verificar que el usuario tenga un perfil de emprendedor
        emprendedor_profile = getattr(request.user, "emprendedor_profile", None)
        if not emprendedor_profile:
            return JsonResponse(
                {"status": "error", "message": "No tienes un perfil de emprendedor."},
                status=403,
            )

        # Buscar el seguimiento asociado al emprendedor
        seguimiento = SeguidorStartup.objects.select_related("startup", "usuario").get(
            pk=seguimiento_id, usuario=emprendedor_profile
        )

        # Verificar que el usuario es quien sigue la startup
        if seguimiento.usuario == emprendedor_profile:
            with transaction.atomic():
                # Eliminar el seguimiento
                seguimiento.delete()

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No tienes permiso para dejar de seguir esta startup",
                },
                status=403,
            )
    except SeguidorStartup.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "No estás siguiendo esta startup."},
            status=404,
        )
    except AttributeError:
        return JsonResponse(
            {"status": "error", "message": "Usuario no autorizado o perfil incompleto"},
            status=403,
        )


@login_required
def modulos_programa(request, programa_id):
    # Obtener el programa
    programa = get_object_or_404(ProgramaPage, id=programa_id)

    # Obtener los módulos del programa
    modulos = Modulo.objects.filter(programa=programa)

    # Contexto para pasar a la plantilla
    context = {
        "programa": programa,
        "modulos": modulos,
    }

    # Renderizar la plantilla con el contexto
    return render(request, "programa_startup/programa_modulo.html", context)


def get_notifications_context(request, max_notificaciones=5, show_all=False):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(usuario=request.user).order_by(
            "-fecha_creacion"
        )
        unread_count = notificaciones.filter(leido=False).count()
        has_notifications = notificaciones.exists()
        has_unread = unread_count > 0

        if not show_all:
            notificaciones = notificaciones[:max_notificaciones]

        notificaciones_html = render_to_string(
            "programa_startup/notificaciones_lista.html",
            {
                "notificaciones": notificaciones,
                "max_notificaciones": max_notificaciones,
                "show_all": show_all,
                "has_notifications": has_notifications,
                "has_unread": has_unread,
                "request": request,  # Make sure this line is present
            },
            request=request,  # Add this line
        )

        return {
            "notificaciones": notificaciones,
            "unread_notifications_count": unread_count,
            "notificaciones_html": notificaciones_html,
            "max_notificaciones": max_notificaciones,
            "show_all": show_all,
            "has_notifications": has_notifications,
            "has_unread": has_unread,
        }
    return {}


# Context processor
def notifications(request):
    return get_notifications_context(request)


@login_required
def ver_notificaciones(request):
    context = get_notifications_context(request, show_all=True)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "notificaciones_html": context["notificaciones_html"],
                "unread_notifications_count": context["unread_notifications_count"],
            }
        )
    return render(request, "programa_startup/notificaciones.html", context)


@login_required
def marcar_todas_leidas(request):
    if request.method == "POST":
        # Marcar todas las notificaciones del usuario como leídas
        request.user.notificacion_set.update(leido=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


@login_required
def eliminar_todas_notificaciones(request):
    if request.method == "POST":
        # Eliminar todas las notificaciones del usuario
        request.user.notificacion_set.all().delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
