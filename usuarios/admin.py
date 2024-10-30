# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import CustomUser, Emprendedor, Mentor, Mentoria
from Aula.sites import aula_admin_site
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import (
    ExportForm,
    ImportForm,
)


class CustomUserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "apellido_paterno",
        "apellido_materno",
        "dni",
        "celular",
        "genero",
        "rol",
        "fecha_nacimiento",
        "foto_perfil",
        "fecha_registro",
        "ultima_sesion",
    ]
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter = ["is_staff", "is_superuser", "is_active", "rol"]
    search_fields = ["username", "email", "dni", "rol"]
    ordering = ["-fecha_registro"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Información personal",
            {
                "fields": (
                    "email",
                    "apellido_paterno",
                    "apellido_materno",
                    "dni",
                    "celular",
                    "genero",
                    "rol",
                    "foto_perfil",
                    "fecha_nacimiento",
                    "ocupacion",
                    "red_social",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                ),
                "classes": ["tab"],
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "apellido_paterno",
                    "apellido_materno",
                    "genero",
                    "rol",
                    "fecha_nacimiento",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class EmprendedorAdmin(ModelAdmin, ImportExportModelAdmin):
    model = Emprendedor
    list_display = [
        "user",
        "startup",
        "universidad",
        "facultad",
        "escuela",
        "grado_instruccion",
        "cargo",
    ]

    import_form_class = ImportForm
    export_form_class = ExportForm

    search_fields = ["user__username", "user__email", "startup__nombre"]

    fieldsets = (
        ("Información básica", {"fields": ("user", "startup"), "classes": ["tab"]}),
        (
            "Información Académica",
            {
                "fields": ("grado_instruccion", "universidad", "facultad", "escuela"),
                "classes": ["tab"],
            },
        ),
        (
            "Perfil Profesional",
            {
                "fields": ("resumen_perfil", "sectores_interes", "habilidades_blandas"),
                "classes": ["tab"],
            },
        ),
    )
    readonly_fields = ["cargo"]


class MentorAdmin(ModelAdmin, ImportExportModelAdmin):
    model = Mentor
    list_display = [
        "user",
        "especialidad",
        "profesion",
        "empresa_a_cargo",
        "pertenece_universidad",
        "es_speaker",
        "get_precio",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "especialidad",
        "profesion",
        "empresa_a_cargo",
    ]

    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        (
            "Información Básica",
            {
                "fields": (
                    "user",
                    "especialidad",
                    "profesion",
                    "biografia",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Información Laboral",
            {
                "fields": ("empresa_a_cargo", "pertenece_universidad", "es_speaker"),
                "classes": ["tab"],
            },
        ),
        (
            "Mentoría",
            {
                "fields": (
                    "programa",
                    "disponibilidad",
                    "sala_virtual",
                    "mentoria_startups",
                    "beneficios",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Información de Pago",
            {"fields": ("puede_cobrar", "precio_por_hora"), "classes": ["tab"]},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["puede_cobrar"]
        return []


class MentoriaAdmin(ModelAdmin, ImportExportModelAdmin):
    model = Mentoria
    list_display = ["mentor", "startup", "fecha", "temas", "estado"]
    list_filter = ["estado", "fecha", "mentor", "startup"]
    search_fields = ["mentor__user__username", "startup__nombre", "temas"]

    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "mentor",
                    "startup",
                    "fecha",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Detalles de la Mentoría",
            {
                "fields": (
                    "temas",
                    "estado",
                ),
                "classes": ["tab"],
            },
        ),
    )

    readonly_fields = [
        "fecha"
    ]  # Asumiendo que no quieres que se edite la fecha una vez creada

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("mentor__user", "startup")  # Optimiza las consultas


aula_admin_site.register(CustomUser, CustomUserAdmin)
aula_admin_site.register(Emprendedor, EmprendedorAdmin)
aula_admin_site.register(Mentor, MentorAdmin)
aula_admin_site.register(Mentoria, MentoriaAdmin)
