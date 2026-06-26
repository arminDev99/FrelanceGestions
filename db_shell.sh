#!/bin/bash

# Cargar variables del .env si existe (o usar valores por defecto del proyecto)
DB_USER=${DB_USER:-admin}
DB_NAME=${DB_NAME:-freelance_db}
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

# Establecer la contraseña para evitar el prompt (usando la del docker-compose/settings)
export PGPASSWORD=${DB_PASSWORD:-adminpass}

echo "Conectando a la base de datos $DB_NAME como $DB_USER..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
