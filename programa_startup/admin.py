from django.contrib import admin
from .models import Startup, IntegranteStartup

class IntegranteStartupInline(admin.TabularInline):
    model = IntegranteStartup
    extra = 1  # Para que aparezca un formulario extra para agregar nuevos integrantes directamente desde la página de administración de Startup
    fields = ['usuario', 'cargo', 'fecha_inscripcion', 'agregado_por']
    readonly_fields = ['fecha_inscripcion']

class StartupAdmin(admin.ModelAdmin):
    model = Startup
    list_display = (
        'nombre', 'fundador', 'fecha_creacion', 'programa', 'descripcion_corta'
    )
    search_fields = ('nombre', 'fundador__username', 'programa__nombre')
    list_filter = ('programa', 'fecha_creacion')
    inlines = [IntegranteStartupInline]

    def descripcion_corta(self, obj):
        return obj.descripcion[:50]  # Muestra los primeros 50 caracteres de la descripción

    descripcion_corta.short_description = 'Descripción'

    fieldsets = (
        (None, {'fields': ('nombre', 'descripcion', 'logo', 'fundador')}),
        ('Detalles del Programa', {'fields': ('programa',)}),
        ('Información Adicional', {'fields': ('problematica', 'propuesta_valor', 'publico_objetivo', 'socios_clave', 'canales', 'producto_servicio')}),
    )

admin.site.register(Startup, StartupAdmin)

class IntegranteStartupAdmin(admin.ModelAdmin):
    model = IntegranteStartup
    list_display = ('usuario', 'startup', 'cargo', 'fecha_inscripcion', 'agregado_por')
    search_fields = ('usuario__username', 'startup__nombre')
    list_filter = ('cargo', 'fecha_inscripcion')

admin.site.register(IntegranteStartup, IntegranteStartupAdmin)