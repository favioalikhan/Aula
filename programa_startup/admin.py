from unfold.admin import ModelAdmin, TabularInline
from django.contrib import admin
from .models import Startup, IntegranteStartup, Entregable, Tarea, ProgramaPage
from Aula.sites import aula_admin_site
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import (
    ExportForm,
    ImportForm,
)
from django.utils.html import format_html


class IntegranteStartupInline(TabularInline):
    model = IntegranteStartup
    extra = 1  # Para que aparezca un formulario extra para agregar nuevos integrantes directamente desde la página de administración de Startup
    fields = ["usuario", "cargo", "fecha_inscripcion", "agregado_por"]
    readonly_fields = ["fecha_inscripcion"]


class StartupAdmin(ModelAdmin, ImportExportModelAdmin):
    model = Startup
    inlines = [IntegranteStartupInline]

    list_display = [
        "nombre",
        "programa",
        "fundador",
        "fecha_creacion",
        "fecha_inscripcion",
        "progreso",
        "activo",
    ]
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter = ["activo", "programa", "fecha_creacion", "fecha_inscripcion"]
    search_fields = ["nombre", "descripcion", "fundador__username"]

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "nombre",
                    "descripcion",
                    "logo",
                    "fundador",
                    "programa",
                    "fecha_inscripcion",
                    "activo",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Modelo de Negocio",
            {
                "fields": (
                    "problematica",
                    "propuesta_valor",
                    "publico_objetivo",
                    "socios_clave",
                    "canales",
                    "producto_servicio",
                ),
                "classes": ["tab"],
            },
        ),
        ("Progreso", {"fields": ("progreso",), "classes": ["tab"]}),
    )

    readonly_fields = ["fecha_creacion", "progreso"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("fundador", "programa")


class IntegranteStartupAdmin(ModelAdmin, ImportExportModelAdmin):
    model = IntegranteStartup
    list_display = ("usuario", "startup", "cargo", "fecha_inscripcion", "agregado_por")
    search_fields = ("usuario__username", "startup__nombre")
    list_filter = ("cargo", "fecha_inscripcion")
    import_form_class = ImportForm
    export_form_class = ExportForm


class ProgramaFilter(admin.SimpleListFilter):
    title = "Programa"
    parameter_name = "programa"

    def lookups(self, request, model_admin):
        if model_admin.model == Tarea:
            programas = ProgramaPage.objects.filter(
                modulos__sprints__sesiones__tareas__isnull=False
            ).distinct()
        else:  # EntregableAdmin
            programas = ProgramaPage.objects.filter(
                modulos__sprints__sesiones__tareas__entregables__isnull=False
            ).distinct()
        return [(p.id, p.titulo) for p in programas]

    def queryset(self, request, queryset):
        if self.value():
            if isinstance(queryset.model, Tarea):
                return queryset.filter(sesion__sprint__modulo__programa_id=self.value())
            return queryset.filter(
                tarea__sesion__sprint__modulo__programa_id=self.value()
            )
        return queryset


class EntregableInline(TabularInline):
    model = Entregable
    extra = 0
    readonly_fields = ["fecha_subida", "subido_por", "get_archivo_link"]
    fields = [
        "startup",
        "get_archivo_link",
        "fecha_subida",
        "subido_por",
        "estado",
        "calificacion",
        "comentario",
    ]

    def get_archivo_link(self, obj):
        if obj.archivo:
            return format_html(
                '<a href="{}" target="_blank">Descargar archivo</a>', obj.archivo.url
            )
        return "Sin archivo"

    get_archivo_link.short_description = "Archivo"

    def has_add_permission(self, request, obj=None):
        return False


class TareaAdmin(ModelAdmin, ImportExportModelAdmin):
    model = Tarea
    inlines = [EntregableInline]

    list_display = [
        "titulo",
        "get_sesion",
        "get_programa",
        "tipo",
        "fecha_inicio",
        "fecha_entrega",
        "get_entregables_count",
        "bloqueado",
    ]

    list_filter = ["tipo", "bloqueado", ProgramaFilter, "fecha_inicio", "fecha_entrega"]

    search_fields = [
        "titulo",
        "descripcion",
        "sesion__titulo",
    ]

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "sesion",
                    "titulo",
                    "tipo",
                    "bloqueado",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Detalles",
            {
                "fields": (
                    "descripcion",
                    "fecha_entrega",
                    "archivo",
                ),
                "classes": ["tab"],
            },
        ),
    )

    def get_sesion(self, obj):
        return obj.sesion.titulo if obj.sesion else "-"

    get_sesion.short_description = "Sesión"

    def get_programa(self, obj):
        return (
            obj.sesion.sprint.modulo.programa.titulo
            if obj.sesion
            and obj.sesion.sprint
            and obj.sesion.sprint.modulo
            and obj.sesion.sprint.modulo.programa
            else "-"
        )

    get_programa.short_description = "Programa"

    def get_entregables_count(self, obj):
        return obj.entregables.count()

    get_entregables_count.short_description = "Entregables"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "sesion",
                "sesion__sprint",
                "sesion__sprint__modulo",
                "sesion__sprint__modulo__programa",
            )
            .prefetch_related("entregables")
        )


class EntregableAdmin(ModelAdmin, ImportExportModelAdmin):
    model = Entregable

    list_display = [
        "get_tarea_titulo",
        "startup",
        "get_programa",
        "estado",
        "fecha_subida",
        "subido_por",
        "calificacion",
        "get_archivo_link",
    ]

    list_filter = [
        "estado",
        "fecha_subida",
        ProgramaFilter,
        "startup",
    ]

    search_fields = [
        "tarea__titulo",
        "startup__nombre",
        "subido_por__username",
        "comentario",
    ]

    readonly_fields = ["fecha_subida", "get_archivo_link"]

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "tarea",
                    "startup",
                    "subido_por",
                    "estado",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Evaluación",
            {
                "fields": (
                    "calificacion",
                    "comentario",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Archivo",
            {
                "fields": (
                    "archivo",
                    "fecha_subida",
                ),
                "classes": ["tab"],
            },
        ),
    )

    def get_tarea_titulo(self, obj):
        return obj.tarea.titulo

    get_tarea_titulo.short_description = "Tarea"

    def get_programa(self, obj):
        return (
            obj.tarea.sesion.sprint.modulo.programa.titulo
            if (
                obj.tarea
                and obj.tarea.sesion
                and obj.tarea.sesion.sprint
                and obj.tarea.sesion.sprint.modulo
                and obj.tarea.sesion.sprint.modulo.programa
            )
            else "-"
        )

    get_programa.short_description = "Programa"

    def get_archivo_link(self, obj):
        if obj.archivo:
            return format_html(
                '<a href="{}" target="_blank">Descargar archivo</a>', obj.archivo.url
            )
        return "Sin archivo"

    get_archivo_link.short_description = "Archivo"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "tarea",
                "startup",
                "subido_por",
                "tarea__sesion",
                "tarea__sesion__sprint",
                "tarea__sesion__sprint__modulo",
                "tarea__sesion__sprint__modulo__programa",
            )
        )


aula_admin_site.register(Startup, StartupAdmin)
aula_admin_site.register(IntegranteStartup, IntegranteStartupAdmin)
aula_admin_site.register(Tarea, TareaAdmin)
aula_admin_site.register(Entregable, EntregableAdmin)
