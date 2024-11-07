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

# Recopilar archivos estáticos