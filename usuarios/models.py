"""
    El código define modelos para la gestión de usuarios, incluidos roles, perfiles para
    emprendedores y mentores, sesiones de tutoría y notificaciones.` proporciona una breve descripción
    o resumen del propósito del código que lo sigue. Indica que el código a continuación define
    modelos de Django relacionados con la gestión de usuarios, roles, perfiles para emprendedores y mentores, sesiones de
    tutoría y notificaciones dentro de un proyecto de Django.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from programa_startup.models import (
    Startup,
    ProgramaPage,
    IntegranteStartup,
)
from django.utils import timezone
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("El Email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("rol", "admin")
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    ADMINISTRADOR = "admin"
    EMPRENDEDOR = "emprendedor"
    MENTOR = "mentor"
    SPEAKER = "speaker"

    ROLE_CHOICES = [
        (ADMINISTRADOR, "Administrador"),
        (EMPRENDEDOR, "Emprendedor"),
        (MENTOR, "Mentor"),
        (SPEAKER, "Speaker"),
    ]

    GENDER_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[],  # Elimina validaciones predeterminadas
    )
    first_name = None
    last_name = None
    dni = models.CharField(max_length=20, unique=True, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50, blank=True, null=True)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    genero = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    rol = models.CharField(max_length=50, choices=ROLE_CHOICES, default=EMPRENDEDOR)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    red_social = models.URLField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ultima_sesion = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definimos los getters y setters dinámicamente
        type(self).first_name = property(
            lambda self: self.username,
            lambda self, value: setattr(self, "username", value),
        )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def save(self, *args, **kwargs):
        # Asegurar que el superusuario tenga el rol de 'Administrador'
        if self.is_superuser:
            self.rol = self.ADMINISTRADOR
            self.is_staff = True

        super().save(*args, **kwargs)

        # Crear perfil de emprendedor, mentor o speaker según el rol seleccionado
        if self.rol == self.EMPRENDEDOR and not hasattr(self, "emprendedor_profile"):
            Emprendedor.objects.create(user=self)
        elif self.rol == self.MENTOR and not hasattr(self, "mentor_profile"):
            Mentor.objects.create(user=self)
        elif self.rol == self.SPEAKER and not hasattr(self, "mentor_profile"):
            # Aquí asumimos que los speakers también tienen un perfil de Mentor para simplicidad
            Mentor.objects.create(user=self, es_speaker=True)

    def clean_username(self):
        # Custom validation to ensure the username does not contain numbers
        if any(char.isdigit() for char in self.username):
            raise ValidationError("El nombre de usuario no debe contener números")

        # Ensure username doesn't contain multiple spaces or special characters
        self.username = re.sub(r"\s+", " ", self.username.strip())  # Normalize spaces
        if re.search(r"[^a-zA-Z\s]", self.username):
            raise ValidationError(
                "El nombre de usuario solo puede contener letras y espacios"
            )

        return self.username

    def clean_dni(self):
        dni = self.cleaned_data.get("dni")
        if len(dni) != 8:
            raise ValidationError("El DNI debe tener 8 dígitos.")
        if not dni.isdigit():
            raise ValidationError("El DNI debe contener solo números.")
        return dni


class Emprendedor(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="emprendedor_profile"
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.SET_NULL, null=True, blank=True
    )
    resumen_perfil = models.TextField(blank=True, null=True)
    grado_instruccion = models.CharField(max_length=100, blank=True, null=True)
    universidad = models.CharField(max_length=100, blank=True, null=True)
    facultad = models.CharField(max_length=100, blank=True, null=True)
    escuela = models.CharField(max_length=100, blank=True, null=True)
    sectores_interes = models.TextField(blank=True, null=True)
    habilidades_blandas = models.TextField(blank=True, null=True)

    @property
    def cargo(self):
        integrante = IntegranteStartup.objects.filter(
            usuario=self.user, startup=self.startup
        ).first()
        return integrante.cargo if integrante else None

    def obtener_startups_seguidas(self):
        return Startup.objects.filter(seguidores_startup__usuario=self)

    class Meta:
        verbose_name = "emprendedor"
        verbose_name_plural = "emprendedores"


class SeguidorStartup(models.Model):
    usuario = models.ForeignKey(
        Emprendedor, on_delete=models.CASCADE, related_name="startups_seguidas"
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name="seguidores_startup"
    )
    fecha_seguimiento = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Verificar si el usuario ya sigue 5 startups
        if SeguidorStartup.objects.filter(usuario=self.usuario).count() >= 5:
            raise ValidationError(
                "Un emprendedor solo puede seguir un máximo de 5 startups."
            )
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "startup"], name="unique_seguidor_startup"
            )
        ]
        verbose_name = "Seguidor-Startup"
        verbose_name_plural = "Seguidores-Startups"


class Mentor(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="mentor_profile"
    )
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    profesion = models.CharField(max_length=100, blank=True, null=True)
    empresa_a_cargo = models.CharField(max_length=100, blank=True, null=True)
    pertenece_universidad = models.BooleanField(default=False)
    beneficios = models.TextField(blank=True, null=True)
    disponibilidad = models.CharField(
        max_length=255, blank=True, null=True
    )  # Ej. "Lunes a Viernes, 9AM-5PM"
    programa = models.ForeignKey(
        ProgramaPage, on_delete=models.SET_NULL, null=True, blank=True
    )
    # programa = models.CharField(max_length=10, blank=True, null=True)
    sala_virtual = models.URLField(
        blank=True, null=True
    )  # URL a la sala de sesión virtual
    mentoria_startups = models.CharField(
        max_length=255, blank=True, null=True
    )  # IDs o nombres de hasta 3 startups
    puede_cobrar = models.BooleanField(
        default=False
    )  # Solo el admin puede cambiar esto
    precio_por_hora = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    es_speaker = models.BooleanField(
        default=False
    )  # Para diferenciar entre Mentor y Speaker

    def __str__(self):
        return f"{self.user.username} - {'Pago' if self.puede_cobrar else 'Gratis'} - Programa: {self.programa.titulo if self.programa else 'No asignado'}"

    def es_mentoria_gratis(self):
        return not self.puede_cobrar or self.precio_por_hora is None

    def get_precio(self):
        if self.es_mentoria_gratis():
            return "Gratis"
        return f"S/.{self.precio_por_hora}"

    class Meta:
        verbose_name = "mentor"
        verbose_name_plural = "mentores"


class Mentoria(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    temas = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ("PENDIENTE", "Pendiente"),
            ("COMPLETADA", "Completada"),
        ],
    )

    # def __str__(self):
    #    return f"Mentoría con {self.mentor.user.username} para {self.startup.nombre}"
    def __str__(self):
        return f"{self.startup.nombre} - {self.temas}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Notificación al mentor

    """
        mensaje_mentor = f"Tienes una mentoría programada con la startup '{self.startup.nombre}' sobre '{self.temas}' en la fecha {self.fecha}."
        Notificacion.objects.create(
            usuario=self.mentor.usuario,  # Asumiendo que Mentor tiene un campo relacionado con el usuario
            tipo="Mentoría",
            mensaje=mensaje_mentor,
        )
        # Notificación a los integrantes de la startup
        for integrante in self.startup.integrantes.all():
            mensaje_integrante = f"Se ha programado una mentoría con '{self.mentor.usuario.username}' sobre '{self.temas}' para la startup '{self.startup.nombre}'."
            Notificacion.objects.create(
                usuario=integrante.usuario, tipo="Mentoría", mensaje=mensaje_integrante
            )
    """
