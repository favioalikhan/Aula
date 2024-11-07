#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -o errexit

# Instalar las dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade wagtail

# Si usas Poetry, descomenta la siguiente línea y comenta las líneas de pip
# poetry install
python manage.py collectstatic --noinput
# Aplicar migraciones de la base de datos
python manage.py migrate

# Crear el superusuario si no existe
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
email = os.getenv('SUPERUSER_EMAIL')
username = os.getenv('SUPERUSER_USERNAME')
password = os.getenv('SUPERUSER_PASSWORD')

if email and username and password:
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, username=username, password=password)
        print("Superusuario creado exitosamente.")
    else:
        print("El superusuario ya existe.")
else:
    print("No se proporcionaron las credenciales del superusuario.")
EOF