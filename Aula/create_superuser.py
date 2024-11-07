import os
import django
from django.contrib.auth import get_user_model

# Configura las variables de entorno si no estás ejecutando esto dentro del entorno de Render
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aula.settings.production")
django.setup()


def create_superuser():
    User = get_user_model()
    email = os.getenv("SUPERUSER_EMAIL")
    username = os.getenv("SUPERUSER_USERNAME")
    password = os.getenv("SUPERUSER_PASSWORD")

    if not email or not username or not password:
        print(
            "Por favor, establece las variables de entorno SUPERUSER_EMAIL, SUPERUSER_USERNAME y SUPERUSER_PASSWORD."
        )
        return

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, username=username, password=password)
        print("Superusuario creado exitosamente.")
    else:
        print("El superusuario ya existe.")


if __name__ == "__main__":
    create_superuser()
