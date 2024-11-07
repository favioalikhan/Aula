#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -o errexit

# Instalar las dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Si usas Poetry, descomenta la siguiente línea y comenta las líneas de pip
# poetry install

# Aplicar migraciones de la base de datos
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput