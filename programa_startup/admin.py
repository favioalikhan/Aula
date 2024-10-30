from unfold.admin import ModelAdmin, TabularInline
from .models import Startup, IntegranteStartup
from Aula.sites import aula_admin_site
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import (
    ExportForm,
    ImportForm,
)


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


aula_admin_site.register(Startup, StartupAdmin)
aula_admin_site.register(IntegranteStartup, IntegranteStartupAdmin)
