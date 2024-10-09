from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Emprendedor, Mentor
from .forms import CustomUserCreationForm, UserCustomChangeForm

# Este código define clases de administración personalizadas para gestionar usuarios, emprendedores y mentores en el admin Django

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = UserCustomChangeForm

    # Campos que se mostrarán en la lista de usuarios
    list_display = (
        'username', 'email', 'apellido_paterno', 'apellido_materno', 
        'dni', 'celular', 'genero', 'rol', 'fecha_nacimiento', 
        'foto_perfil', 'fecha_registro', 'ultima_sesion'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol')

    # Campos para editar en el formulario de administración
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': (
            'email', 'apellido_paterno', 'apellido_materno', 'dni', 
            'celular', 'genero', 'rol', 'foto_perfil', 'fecha_nacimiento','ocupacion', 'red_social'
        )}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'apellido_paterno', 'apellido_materno', 'genero', 'rol','fecha_nacimiento', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'dni', 'rol')
    ordering = ('-fecha_registro',)
    
# Registro del modelo Emprendedor
class EmprendedorAdmin(admin.ModelAdmin):
    model = Emprendedor
    list_display = ('user', 'startup', 'universidad', 'facultad', 'escuela', 'grado_instruccion', 'get_startups_seguidas' )
    search_fields = ('user__username', 'user__email', 'startup')
    fieldsets = (
        (None, {'fields': ('user', 'startup', 'grado_instruccion', 'universidad', 'facultad', 'escuela','sectores_interes', 'habilidades_blandas')}),
    )
    def get_startups_seguidas(self, obj):
        # Obtiene las startups seguidas y las muestra como una cadena
        return ', '.join([startup.nombre for startup in obj.obtener_startups_seguidas()])
    get_startups_seguidas.short_description = 'Startups Seguidas'


# Registro del modelo Mentor
class MentorAdmin(admin.ModelAdmin):
    model = Mentor
    list_display = ('user', 'especialidad', 'profesion', 'empresa_a_cargo', 'pertenece_universidad')
    search_fields = ('user__username', 'user__email', 'especialidad')
    fieldsets = (
        (None, {'fields': ('user', 'especialidad', 'biografia', 'profesion', 'empresa_a_cargo', 'pertenece_universidad', 'beneficios', 'disponibilidad','programa', 'puede_cobrar', 'precio_por_hora', 'sala_virtual', 'mentoria_startups')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Emprendedor, EmprendedorAdmin)
admin.site.register(Mentor, MentorAdmin)