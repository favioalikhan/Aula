"""
    El código define modelos que incluyen ProgramaPage, Startup, Modulo, Sprint, Sesion, Tarea, 
    Entregable, Evento, IntegranteStartup y Logro con varios campos y
    relaciones.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from django.conf import settings

# Wagtail
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

# wagtail_admin-------------------------------------------------------------------------------


# Beneficios del programa
class ProgramaBeneficio(models.Model):
    page = ParentalKey(
        "ProgramaPage", related_name="beneficios", on_delete=models.CASCADE
    )
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    descripcion = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("imagen"),
        FieldPanel("descripcion"),
    ]


class CriterioEvaluacion(models.Model):
    page = ParentalKey(
        "ProgramaPage", related_name="criterios", on_delete=models.CASCADE
    )
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    descripcion = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("imagen"),
        FieldPanel("descripcion"),
    ]


class CronogramaItem(models.Model):
    page = ParentalKey(
        "CronogramaPrograma", related_name="items", on_delete=models.CASCADE
    )
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Imagen del proceso",
    )
    nombre_proceso = models.CharField(max_length=255, help_text="Nombre del proceso")
    fecha_inicio = models.DateField(help_text="Fecha de inicio del proceso")
    fecha_fin = models.DateField(help_text="Fecha de finalización del proceso")

    panels = [
        FieldPanel("imagen"),
        FieldPanel("nombre_proceso"),
        FieldPanel("fecha_inicio"),
        FieldPanel("fecha_fin"),
    ]


class CronogramaPrograma(ClusterableModel):
    page = ParentalKey(
        "ProgramaPage", related_name="cronograma", on_delete=models.CASCADE
    )
    modalidad = models.CharField(
        max_length=20,
        choices=[
            ("Presencial", "Presencial"),
            ("Virtual", "Virtual"),
            ("Híbrido", "Híbrido"),
        ],
        help_text="Modalidad del programa",
    )
    frecuencia = models.CharField(max_length=255, help_text="Frecuencia de clase")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("modalidad"),
                FieldPanel("frecuencia"),
                InlinePanel("items", label="Cronograma"),
            ],
            heading="Cronograma del Programa",
        ),
    ]


class ProgramaPage(Page):
    # Campos principales del programa
    titulo = models.CharField(max_length=255, help_text="Título del programa")
    descripcion = RichTextField(blank=True, help_text="Descripción del programa")
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Imagen del programa",
    )
    requisitos = RichTextField(
        blank=True, help_text="Requisitos para participar en el programa"
    )
    """
    def serve(self, request):
        # Obtener todos los módulos hijos de esta página
        modulos = Modulo.objects.child_of(self).live()

        # Pasar los módulos al contexto
        return render(request, "programa_startup/modulo.html", {
            "page": self,
            "modulos": modulos
        })
    """

    @property
    def is_active(self):
        # Obtiene el primer objeto CronogramaPrograma asociado con ProgramaPage
        cronograma = self.cronograma.first()
        if cronograma and cronograma.items.exists():
            # Obtiene el primer objeto CronogramaItem del CronogramaPrograma
            item = cronograma.items.first()
            if item and item.fecha_inicio and item.fecha_fin:
                return item.fecha_inicio <= timezone.now().date() <= item.fecha_fin
        return False

    content_panels = Page.content_panels + [
        FieldPanel("titulo"),
        FieldPanel("descripcion"),
        FieldPanel("imagen"),
        MultiFieldPanel(
            [
                InlinePanel("beneficios", label="Beneficios"),
            ],
            heading="Beneficios del Programa",
        ),
        InlinePanel("cronograma", label="Cronograma"),
        FieldPanel("requisitos"),
        MultiFieldPanel(
            [
                InlinePanel("criterios", label="Criterios de Evaluación"),
            ],
            heading="Criterios de Evaluación",
        ),
    ]

    class Meta:
        verbose_name = "Programa Page"
        verbose_name_plural = "Programas Page"

    def save(self, *args, **kwargs):
        # is_new = self.pk is None
        super().save(*args, **kwargs)
        # if is_new:
        #    self.notificar_nuevo_programa()

    @classmethod
    def create_programa(cls, title, parent):
        slug = slugify(title)
        programa = cls(title=title, slug=slug)
        parent.add_child(instance=programa)
        return programa


# Notificacion
class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("Tarea", "Tarea"),
            ("Equipo", "Equipo"),
            ("Evento", "Evento"),
            ("Mentoria", "Mentoria"),
        ],
    )
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo}: {self.mensaje} | Para: {self.usuario.username}"


# Startup-----------------------------------------------------------------------------------
class Startup(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="logos_startups/", blank=True, null=True)
    problematica = models.TextField(blank=True)
    propuesta_valor = models.TextField(blank=True)
    publico_objetivo = models.TextField(blank=True)
    socios_clave = models.TextField(blank=True)
    canales = models.TextField(blank=True, null=True)
    producto_servicio = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    programa = models.ForeignKey(
        ProgramaPage,
        on_delete=models.CASCADE,
        related_name="program_startups",
        null=True,
        blank=True,
    )
    fecha_inscripcion = models.DateTimeField(null=True, blank=True)
    progreso = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    activo = models.BooleanField(default=True)
    fundador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="startup_fundador",
    )
    integrantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="IntegranteStartup",
        related_name="startups_integrante",
        through_fields=("startup", "usuario"),
    )

    def __str__(self):
        return self.nombre

    def calcular_progreso(self):
        if not self.programa:
            return 0.0

        total_progreso = 0.0
        total_peso = 0.0

        modulos = self.programa.modulos.all()
        total_modulos = modulos.count()

        for modulo in modulos:
            peso_modulo = 100.0 / total_modulos
            sprints = modulo.sprints.all()
            total_sprints = sprints.count()

            for sprint in sprints:
                peso_sprint = peso_modulo / total_sprints
                sesiones = sprint.sesiones.all()
                total_sesiones = sesiones.count()

                for sesion in sesiones:
                    peso_sesion = peso_sprint / total_sesiones
                    tareas = sesion.tareas.filter(
                        tipo="tarea"
                    )  # Solo consideramos tareas, no recursos
                    total_tareas = tareas.count()

                    if total_tareas > 0:
                        entregables_completados = Entregable.objects.filter(
                            tarea__in=tareas, startup=self, estado="revisado"
                        ).count()
                        progreso_sesion = (
                            entregables_completados / total_tareas
                        ) * peso_sesion
                        total_progreso += progreso_sesion

            total_peso += peso_modulo

        self.progreso = (total_progreso / total_peso) * 100.0 if total_peso > 0 else 0.0
        self.save(update_fields=["progreso"])

    def save(self, *args, **kwargs):
        # Lógica adicional para verificar si la inscripción es válida
        if self.programa:
            cronograma = self.programa.cronograma.first()
            if cronograma and cronograma.items.exists():
                fecha_fin = cronograma.items.order_by("-fecha_fin").first().fecha_fin
                if fecha_fin and timezone.now().date() > fecha_fin:
                    raise ValueError(
                        "No se puede inscribir en un programa que ya ha terminado"
                    )

            # Verifica si el programa está activo; si no, desactiva la inscripción
            if not self.programa.is_active:
                self.activo = False

        super().save(*args, **kwargs)  # Guardar la instancia

    class Meta:
        verbose_name = "startup"
        verbose_name_plural = "startups"


# Campos-Programa---------------------------------------------------------------------------------
class Modulo(Page):
    programa = ParentalKey(
        "ProgramaPage",
        on_delete=models.SET_NULL,
        related_name="modulos",
        null=True,
        blank=True,
    )
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="modulos/", null=True, blank=True)

    class Meta:
        verbose_name = "módulo"
        verbose_name_plural = "módulos"

    content_panels = Page.content_panels + [
        FieldPanel("titulo"),
        FieldPanel("descripcion"),
        FieldPanel("imagen"),
        InlinePanel("sprints", label="Sprints"),
    ]

    @property
    def programa_id(self):
        # Obtiene la página padre y asegura que sea de tipo ProgramaPage
        parent = self.get_parent().specific
        if isinstance(parent, ProgramaPage):
            return parent.id
        return None


class Sprint(ClusterableModel):
    modulo = ParentalKey("Modulo", on_delete=models.CASCADE, related_name="sprints")
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.titulo} - {self.modulo.titulo}"

    class Meta:
        verbose_name = "sprint"
        verbose_name_plural = "sprints"

    panels = [
        FieldPanel("titulo"),
        FieldPanel("descripcion"),
        InlinePanel("sesiones", label="Sesiones"),
    ]


class Sesion(ClusterableModel):
    sprint = ParentalKey("Sprint", on_delete=models.CASCADE, related_name="sesiones")
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("video", "Video"),
            ("lectura", "Lectura"),
            ("ejercicio", "Ejercicio"),
            ("material", "Material Adicional"),
        ],
    )
    archivo = models.FileField(upload_to="sesiones/", blank=True, null=True)
    url_externa = models.URLField(
        max_length=255, blank=True, null=True
    )  # URL externa opcional

    def __str__(self):
        return f"{self.titulo} - {self.sprint.titulo} ({self.tipo})"

    class Meta:
        verbose_name = "sesión"
        verbose_name_plural = "sesiones"

    panels = [
        FieldPanel("titulo"),
        FieldPanel("tipo"),
        FieldPanel("archivo"),
        FieldPanel("url_externa"),
    ]


class Tarea(models.Model):
    TIPO_CHOICES = [
        ("tarea", "Tarea"),
        ("recurso", "Recurso"),
    ]

    BLOQUEADO_CHOICES = [
        ("si", "Sí"),
        ("no", "No"),
    ]

    sesion = models.ForeignKey(
        "Sesion", on_delete=models.CASCADE, related_name="tareas"
    )
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to="tareas/", blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="tarea")
    bloqueado = models.CharField(max_length=2, choices=BLOQUEADO_CHOICES, default="no")

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # Si es un recurso, no necesita fecha de entrega ni descripción
        if self.tipo == "recurso":
            self.fecha_entrega = None
            self.descripcion = None
        super().save(*args, **kwargs)
        self.notificar_integrantes_startup()

    def notificar_integrantes_startup(self):

        # Notificar a los integrantes de la startup sobre la nueva tarea
        programa = self.sesion.sprint.modulo.programa
        # startups = Startup.objects.filter(programa=self.sesion.sprint.modulo.programa)
        integrantes = IntegranteStartup.objects.filter(startup__programas=programa)
        # for startup in startups:
        #    for integrante in startup.integrantes.all():
        #        mensaje = f"Se ha asignado la tarea '{self.titulo}' en la sesión '{self.sesion.titulo}' del programa '{self.sesion.sprint.modulo.programa.titulo}'."
        #        Notificacion.objects.create(
        #            usuario=integrante,
        #            tipo='Tarea',
        #            mensaje=mensaje
        #        )
        # Crear la notificación para cada integrante
        for integrante in integrantes:
            mensaje = f"Nueva tarea asignada: {self.titulo} en la sesión {self.sesion.titulo}."
            Notificacion.objects.create(
                usuario=integrante.usuario, tipo="Tarea", mensaje=mensaje
            )

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"


class Entregable(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("enviado", "Enviado"),
        ("revisado", "Revisado"),
    ]

    tarea = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name="entregables"
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name="startup_entregables"
    )
    archivo = models.FileField(upload_to="entregables/")
    fecha_subida = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=10, choices=ESTADO_CHOICES, default="pendiente"
    )
    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entregables_subidos",
    )
    calificacion = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entregable de {self.startup.nombre} subido por {self.subido_por.username} en {self.tarea.titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Notificar a los demás integrantes sobre el nuevo entregable
        for integrante in self.startup.integrantes.exclude(id=self.subido_por.id):
            mensaje = f"{self.subido_por.username} ha subido un entregable para la tarea '{self.tarea.titulo}' de la startup '{self.startup.nombre}'."
            Notificacion.objects.create(
                usuario=integrante, tipo="Entregable", mensaje=mensaje
            )


class Evento(Page):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    tipo = models.CharField(
        max_length=50, choices=[("Programa", "Programa"), ("General", "General")]
    )
    url_externa = models.URLField(max_length=255, blank=True, null=True)
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Imagen del evento",
    )

    content_panels = Page.content_panels + [
        FieldPanel("titulo"),
        FieldPanel("descripcion"),
        FieldPanel("fecha"),
        FieldPanel("tipo"),
        FieldPanel("url_externa"),
        FieldPanel("imagen"),
    ]

    @property
    def bloqueado(self):
        return self.fecha < timezone.now()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Enviar notificaciones a todos los emprendedores y mentores
        self.notificar_usuarios()

    def notificar_usuarios(self):

        # Filtra los usuarios mentores y emprendedores
        usuarios = settings.AUTH_USER_MODEL.objects.filter(
            role__in=["Mentor", "Emprendedor"]
        )

        # Crea una notificación para cada usuario
        for usuario in usuarios:
            mensaje = f"Nuevo evento disponible: {self.titulo}. Fecha: {self.fecha.strftime('%d/%m/%Y')}."
            Notificacion.objects.create(usuario=usuario, tipo="Evento", mensaje=mensaje)

    class Meta:
        verbose_name = "Evento Page"
        verbose_name_plural = "Eventos Pages"


# Campos-Startup-------------------------------------------------------------------------------------


class IntegranteStartup(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="integrante"
    )
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name="startup_perteneciente"
    )
    cargo = models.CharField(max_length=50)
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    agregado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="startups_agregados",
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo} en {self.startup.nombre}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "startup"], name="unique_usuario_startup"
            )
        ]
        verbose_name = "Usuario-Startup"
        verbose_name_plural = "Usuarios-Startups"


# logro
class Logro(models.Model):
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name="logros"
    )
    titulo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_logro = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.startup.nombre}"

    class Meta:
        verbose_name = "logro"
        verbose_name_plural = "logros"

    def contar_logros(self):
        return self.logros.count()