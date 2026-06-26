# RootDev Backend

Backend de **RootDev**, una aplicación Django para gestionar clientes, proyectos y tareas de trabajo freelance. Incluye panel web, autenticación, vistas con HTMX, Kanban con drag and drop y una API REST con Django REST Framework.

## Características

- Autenticación de usuarios con login, logout y registro.
- Dashboard con resumen de clientes y proyectos activos.
- Gestión de clientes.
- Gestión de proyectos asociados a cada cliente.
- Tablero Kanban para tareas con estados `todo`, `doing` y `done`.
- API REST protegida por sesión.
- Soporte para PostgreSQL local y en Railway.
- Soporte para despliegue con Docker y `gunicorn`.

## Tecnologías

- Python 3.11
- Django
- Django REST Framework
- PostgreSQL
- HTMX
- SortableJS
- Tailwind CSS por CDN
- WhiteNoise
- Gunicorn

## Estructura

```text
backend/
├── config/                # Configuración principal de Django
├── freelance_core/        # App principal: modelos, vistas, API, tests
├── templates/             # Plantillas HTML
├── Dockerfile            # Imagen para despliegue
├── requirements.txt      # Dependencias de Python
├── manage.py             # Comando principal de Django
└── README.md             # Este documento
```

## Requisitos

- Python 3.11 o superior
- PostgreSQL 13+
- `pip`
- Opcional: Docker

## Variables de entorno

El proyecto carga variables desde `.env` ubicado en la raíz del backend.

### Variables principales

```env
SECRET_KEY=una_clave_segura
DEBUG=1

# Opción 1: DATABASE_URL
DATABASE_URL=postgresql://usuario:password@localhost:5432/freelance_db

# Opción 2: variables individuales
DB_NAME=freelance_db
DB_USER=admin
DB_PASSWORD=adminpass
DB_HOST=localhost
DB_PORT=5432
```

### Para Railway

Railway puede inyectar variables como:

```env
DATABASE_URL=postgresql://...
```

o bien:

```env
PGHOST=...
PGDATABASE=...
PGUSER=...
PGPASSWORD=...
PGPORT=5432
```

Si usas Railway detrás de HTTPS, también es recomendable definir:

```env
DEBUG=0
CSRF_TRUSTED_ORIGINS=https://tu-dominio.up.railway.app
RAILWAY_PUBLIC_DOMAIN=tu-dominio.up.railway.app
```

## Instalación local

### 1. Clonar el repositorio

```bash
git clone <URL-DEL-REPOSITORIO>
cd backend
```

### 2. Crear y activar el entorno virtual

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env`

```env
SECRET_KEY=django-insecure-change-me
DEBUG=1
DB_NAME=freelance_db
DB_USER=admin
DB_PASSWORD=adminpass
DB_HOST=localhost
DB_PORT=5432
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Abre:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Ejecución con Docker

```bash
docker build -t rootdev-backend .
docker run --rm -p 8000:8000 --env-file .env rootdev-backend
```

## Despliegue en Railway

1. Sube el código a GitHub.
2. Crea un proyecto en Railway.
3. Conecta el repositorio.
4. Agrega un servicio PostgreSQL.
5. Configura las variables de entorno del servicio web:
   - `SECRET_KEY`
   - `DEBUG=0`
   - `DATABASE_URL` o las variables `PG*`
   - `CSRF_TRUSTED_ORIGINS` si vas a usar un dominio propio
6. Despliega.
7. Abre el shell del servicio y crea el superusuario:

```bash
python manage.py createsuperuser
```

## Rutas principales

### Web

- `/` - Dashboard
- `/login/` - Inicio de sesión
- `/logout/` - Cerrar sesión
- `/register/` - Registro
- `/clientes/` - Listado de clientes
- `/proyectos/` - Listado de proyectos
- `/tareas/` - Tablero Kanban
- `/admin/` - Panel de administración

### API REST

- `/api/clients/`
- `/api/projects/`
- `/api/tasks/`
- `/api/dashboard/`

## Modelos

- `Client`
  - pertenece a un usuario
  - nombre, email, empresa, teléfono, fecha de creación
- `Project`
  - pertenece a un cliente
  - nombre, descripción, estado, fechas de inicio/fin
- `Task`
  - pertenece a un proyecto
  - nombre, prioridad, estado, fecha de entrega

## Pruebas

Ejecutar la suite:

```bash
python manage.py test freelance_core
```

La suite cubre:

- creación de clientes
- creación de proyectos
- creación de tareas
- borrado en cascada
- redirección cuando no hay sesión
- login correcto
- registro de usuarios

## Comandos útiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test freelance_core
python manage.py collectstatic --noinput
```

## Scripts del proyecto

- `./run.sh` inicia el servidor de desarrollo.
- `./test.sh` ejecuta la suite de pruebas de `freelance_core`.
- `./db_shell.sh` abre `psql` contra la base configurada.

## Notas importantes

- El backend usa PostgreSQL; no está pensado para SQLite como base principal.
- `DATABASE_URL` tiene prioridad sobre `DB_*`.
- Si Railway te devuelve un error CSRF, revisa `SECRET_KEY`, `CSRF_TRUSTED_ORIGINS` y el dominio público del servicio.
- Los formularios con HTMX y `fetch` usan la cookie `csrftoken`.
