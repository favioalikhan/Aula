import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin
from usuarios.models import CustomUser, Emprendedor, Mentor, Mentoria
from programa_startup.models import Evento, Startup, ProgramaPage
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from datetime import datetime


class HomeView(RedirectView):
    pattern_name = "admin:index"


class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Custom Title"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "aula/driver_custom_page.html"


def dashboard_callback(request, context):
    MONTHS = [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Oct",
        "Nov",
        "Dic",
    ]

    total_emprendedores = Emprendedor.objects.count()
    total_mentores = Mentor.objects.count()
    total_mentorias = Mentoria.objects.count()
    total_eventos = Evento.objects.count()
    total_startups = Startup.objects.count()
    total_programas = ProgramaPage.objects.count()

    # Mentorias
    # Obtener el año actual
    current_date = datetime.now()

    # Consultar las mentorías completadas del año
    mentorias_completadas = (
        Mentoria.objects.filter(fecha__year=current_date.year, estado="COMPLETADA")
        .annotate(mes=ExtractMonth("fecha"))
        .values("mes")
        .annotate(total=Count("id"))
        .order_by("mes")
    )

    # Consultar las mentorías pendientes del año
    mentorias_pendientes = (
        Mentoria.objects.filter(fecha__year=current_date.year, estado="PENDIENTE")
        .annotate(mes=ExtractMonth("fecha"))
        .values("mes")
        .annotate(total=Count("id"))
        .order_by("mes")
    )

    # Crear diccionarios para almacenar los totales por mes
    completadas_por_mes = {item["mes"]: item["total"] for item in mentorias_completadas}
    pendientes_por_mes = {item["mes"]: item["total"] for item in mentorias_pendientes}

    # Crear lista ordenada de meses
    data_por_mes = []
    for mes_num in range(1, 13):  # 1 al 12
        data_por_mes.append(
            {
                "mes": MONTHS[
                    mes_num - 1
                ],  # Restamos 1 porque los índices empiezan en 0
                "completadas": completadas_por_mes.get(mes_num, 0),
                "pendientes": pendientes_por_mes.get(mes_num, 0),
                "total": completadas_por_mes.get(mes_num, 0)
                + pendientes_por_mes.get(mes_num, 0),
            }
        )
    # --------------
    #  Startups
    # Número máximo de startups a mostrar por página
    STARTUPS_PER_PAGE = 5
    # Obtener página actual de la URL o default a 1
    try:
        current_page = int(request.GET.get("page", 1))
    except (TypeError, ValueError):
        current_page = 1

    startups_activas = (
        Startup.objects.filter(
            programa__isnull=False  # Solo startups con programa asignado
        )
        .select_related("programa")  # Optimización de consulta
        .order_by("-progreso")
    )

    # Crear el paginador
    paginator = Paginator(startups_activas, STARTUPS_PER_PAGE)

    try:
        # Obtener la página actual
        startups_page = paginator.page(current_page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        startups_page = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página
        startups_page = paginator.page(paginator.num_pages)
    # Crear lista de progreso de startups
    progress = []
    for startup in startups_page:
        logo_url = (
            startup.logo.url if startup.logo else "/static/img/default-startup.png"
        )
        programa_title = startup.programa.title if startup.programa else "Sin programa"
        nombre = startup.nombre if startup.nombre else "Startup sin nombre"
        progreso = round(
            startup.progreso or 0, 1
        )  # Valor predeterminado de 0 si `progreso` es None

        progress.append(
            {
                "title": mark_safe(
                    f'<img src="{logo_url}" alt="{nombre} logo" class="inline-block h-6 w-6 mr-2"> {nombre} - {programa_title}'
                ),
                "description": f"Progreso: {progreso}%",
                "value": progreso,
            }
        )
    # Extraer la distribución de roles y géneros de CustomUser
    roles_count = CustomUser.objects.values("rol").annotate(total=Count("rol"))
    gender_count = CustomUser.objects.values("genero").annotate(total=Count("genero"))

    # Preparar datos para gráfico de roles
    roles_labels = [dict(CustomUser.ROLE_CHOICES)[item["rol"]] for item in roles_count]
    roles_data = [item["total"] for item in roles_count]

    # Preparar datos para gráfico de géneros
    gender_labels = ["Masculino", "Femenino", "Otro"]
    gender_data = [
        next((item["total"] for item in gender_count if item["genero"] == "M"), 0),
        next((item["total"] for item in gender_count if item["genero"] == "F"), 0),
        next((item["total"] for item in gender_count if item["genero"] == "O"), 0),
    ]

    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "active": True},
            ],
            "filters": [
                {"title": _("All"), "active": True},
            ],
            "kpi": [
                {
                    "title": mark_safe(
                        '<div class="flex items-center text-sm"><span class="text-center">Mentorías</span>&nbsp; <span class="material-symbols-outlined">question_answer</span></div>'
                    ),
                    "metric": total_mentorias,
                    "footer": mark_safe("Total"),
                },
                {
                    "title": mark_safe(
                        '<div class="flex items-center text-sm"><span class="text-center">Mentores</span>&nbsp; <span class="material-symbols-outlined">supervisor_account</span></div>'
                    ),
                    "metric": total_mentores,
                    "footer": mark_safe("Total"),
                },
                {
                    "title": mark_safe(
                        '<div class="flex items-center text-sm"><span class="text-center">Emprendedores</span>&nbsp; <span class="material-symbols-outlined">business</span></div>'
                    ),
                    "metric": total_emprendedores,
                    "footer": mark_safe("Total"),
                },
                {
                    "title": mark_safe(
                        '<div class="flex items-center text-sm"><span class="text-center">Startups</span>&nbsp; <span class="material-symbols-outlined">rocket</span></div>'
                    ),
                    "metric": total_startups,  # Ejemplo de cantidad total
                    "footer": mark_safe("Total"),
                },
                {
                    "title": mark_safe(
                        '<div class="flex items-center text-sm"><span class="text-center">Eventos</span>&nbsp; <span class="material-symbols-outlined">event</span></div>'
                    ),
                    "metric": total_eventos,
                    "footer": mark_safe("Total"),
                },
                {
                    "title": mark_safe(
                        '<div class="flex items-center text-sm"><span class="text-center">Programas</span>&nbsp; <span class="material-symbols-outlined">workspaces</span></div>'
                    ),
                    "metric": total_programas,
                    "footer": mark_safe("Total"),
                },
            ],
            # Progreso de las startups
            "progress": progress,
            "has_previous": startups_page.has_previous(),
            "has_next": startups_page.has_next(),
            "current_page": current_page,
            "total_pages": paginator.num_pages,
            "page_range": paginator.get_elided_page_range(
                current_page, on_each_side=1, on_ends=1
            ),
            #
            "chart": json.dumps(
                {  # Tendencias de mentorias
                    "labels": [item["mes"] for item in data_por_mes],
                    "datasets": [
                        {
                            "label": "Total Mentorías",
                            "type": "line",
                            "data": [item["total"] for item in data_por_mes],
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                        {
                            "label": "Mentorías Completadas",
                            "data": [item["completadas"] for item in data_por_mes],
                            "backgroundColor": "#9333ea",
                        },
                        {
                            "label": "Mentorías Pendientes",
                            "data": [item["pendientes"] for item in data_por_mes],
                            "backgroundColor": "#f43f5e",
                        },
                    ],
                }
            ),
            "performance": [
                {  # DISTRIBUCION DE ROLES
                    "title": _("Distribución de Roles"),
                    "metric": f"{sum(roles_data)} usuarios",
                    "chart": json.dumps(
                        {
                            "labels": roles_labels,
                            "datasets": [
                                {
                                    "data": roles_data,
                                    "backgroundColor": [
                                        "#1f77b4",
                                        "#ff7f0e",
                                        "#2ca02c",
                                        "#d62728",
                                    ],
                                }
                            ],
                        }
                    ),
                },
                {
                    # DISTRIBUCION DE GENERO
                    "title": _("Distribución de Género"),
                    "metric": f"{sum(gender_data)} usuarios",
                    "chart": json.dumps(
                        {
                            "labels": gender_labels,
                            "datasets": [
                                {
                                    "data": gender_data,
                                    "backgroundColor": [
                                        "#4c51bf",
                                        "#ed64a6",
                                        "#9f7aea",
                                    ],
                                }
                            ],
                        }
                    ),
                },
            ],
        },
    )

    return context
