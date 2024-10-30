from django.apps import AppConfig
from wagtail.users.apps import WagtailUsersAppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"


class CustomWagtailUsersConfig(WagtailUsersAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtail.users"
    user_viewset = "usuarios.viewsets.CustomUserViewSet"
