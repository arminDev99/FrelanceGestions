#!/bin/bash

# Activar el entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar el servidor de desarrollo
python manage.py runserver
