#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Instalar las dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migraciones de la base de datos
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
