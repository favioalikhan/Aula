from django.urls import path
from . import views
from .views import ProgramaModuloView, SubirEntregableView, EditProfileStartup

urlpatterns = [
    # otras rutas
    path("register-startup/", views.crear_startup, name="register-startup"),
    path("edit-startup/", EditProfileStartup.as_view(), name="edit-profile-startup"),
    path(
        "startup/eliminar/<int:startup_id>/",
        views.eliminar_startup,
        name="eliminar-startup",
    ),
    path("salir-startup/<int:startup_id>/", views.salir_startup, name="salir-startup"),
    path(
        "eliminar-integrante/<int:integrante_id>/",
        views.eliminar_integrante,
        name="eliminar_integrante",
    ),
    path(
        "programa/inscribirse/<int:programa_id>/",
        views.inscribir_startup,
        name="inscribir-startup",
    ),
    path("buscar-integrante/", views.search_integrante, name="buscar_integrante"),
    path("profile-startup/", views.profile_startup, name="profile-startup"),
    # -------crear sesiones y tareas----------------------------------------------------------------------
    path("crear-sesion/<int:sprint_id>/", views.crear_sesion, name="crear-sesion"),
    path("crear-tarea/<int:sesion_id>/", views.crear_tarea, name="crear-tarea"),
    path("entregables/<int:tarea_id>/", views.ver_entregables, name="ver-entregables"),
    path(
        "entregables/calificar/<int:pk>/",
        views.calificar_resolucion,
        name="calificar-resolucion",
    ),
    path("sesion/editar/<int:pk>/", views.editar_sesion, name="editar-sesion"),
    path("tarea/editar/<int:pk>/", views.editar_tarea, name="editar-tarea"),
    path("<slug:slug>/modulos/", ProgramaModuloView.as_view(), name="programa-modulo"),
    path("modulos/<int:programa_id>/", views.modulos_programa, name="modulos-programa"),
    path("eliminar-sesion/<int:pk>/", views.eliminar_sesion, name="eliminar-sesion"),
    path("eliminar-tarea/<int:pk>/", views.eliminar_tarea, name="eliminar-tarea"),
    # ----------------calificar tarea
    path(
        "resoluciones/<int:pk>/calificar/",
        views.calificar_resolucion,
        name="calificar-resolucion",
    ),
    # startup-entregable
    path(
        "subir-entregable/<int:tarea_id>/",
        SubirEntregableView.as_view(),
        name="subir-entregable",
    ),
    path(
        "borrar-entregable/<int:pk>/", views.borrar_entregable, name="borrar-entregable"
    ),
    # listar
    path("comunidad/", views.listar_todos, name="listar-todos"),
    path("eventos/", views.eventos_view, name="eventos"),
    path(
        "seguir-startup/<int:startup_id>/", views.seguir_startup, name="seguir-startup"
    ),
    path(
        "dejar-seguir-startup/<int:seguimiento_id>/",
        views.dejar_de_seguir_startup,
        name="dejar-seguir-startup",
    ),
    # notificaciones
    path("ver-notificaciones/", views.ver_notificaciones, name="lista-notificaciones"),
    path(
        "notificaciones/marcar-todas-leidas/",
        views.marcar_todas_leidas,
        name="marcar-todas-leidas",
    ),
    path(
        "notificaciones/eliminar-todas/",
        views.eliminar_todas_notificaciones,
        name="eliminar-todas-notificaciones",
    ),
]
