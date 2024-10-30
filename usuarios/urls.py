from django.urls import path
from .views import EditProfile, SolicitarMentoriaView, CustomLoginView
from django.contrib.auth import views as auth_views
from . import views
from .viewsets import CustomAccountView

urlpatterns = [
    path(
        "account/",
        CustomAccountView.as_view(),
        name="wagtailadmin_account",
    ),
    path(
        "login/",
        CustomLoginView.as_view(template_name="usuarios/login.html"),
        name="login",
    ),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", EditProfile.as_view(), name="edit-profile"),
    path("delete-account/", views.delete_account, name="eliminar-cuenta"),
    path("ruta-emprendedor/", views.ruta_emprendedor, name="ruta-emprendedor"),
    path(
        "solicitar-mentoria/<int:mentor_id>/",
        SolicitarMentoriaView.as_view(),
        name="solicitar-mentoria",
    ),
    path(
        "cancelar-mentoria/<int:mentoria_id>/",
        views.cancelar_mentoria,
        name="cancelar-mentoria",
    ),
    path(
        "marcar-mentoria-completada/",
        views.marcar_mentoria_completada,
        name="marcar-mentoria-completada",
    ),
    path("password-reset/", views.password_reset_request, name="password-reset"),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="usuarios/password_reset_done.html"
        ),
        name="password-reset-done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="usuarios/password_reset_confirm.html"
        ),
        name="password-reset-confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="usuarios/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
