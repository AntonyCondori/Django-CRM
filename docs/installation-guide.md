# Configuración del Proyecto

## Requisitos Previos

Antes de iniciar, asegúrate de tener instalado:

* Git
* Node.js
* pnpm
* Python 3.12+
* PostgreSQL
* pgAdmin 4 (opcional para administrar la base de datos)

---

# Frontend

## Instalar dependencias

```bash
cd frontend
pnpm install
```

## Ejecutar el frontend

```bash
pnpm run dev
```

El frontend estará disponible en la URL indicada por Vite (generalmente `http://localhost:5173`).

---

# Backend

## Instalar UV

Ejecutar en PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificar la instalación:

```powershell
uv --version
```

### Si se cierra la consola

Agregar temporalmente la ruta de UV:

```powershell
$env:Path = "C:\Users\Usuario\.local\bin;$env:Path"
```

---

## Configurar variables de entorno

Copiar el archivo de ejemplo:

```powershell
copy .env.example .env
```

Editar el archivo `.env` y configurar los datos de la base de datos:

```env
DBNAME="crm_db"
DBUSER="postgres"
DBPASSWORD="TU_CONTRASEÑA"
DBHOST="localhost"
DBPORT="5432"
```

---

## Crear la Base de Datos

Antes de ejecutar las migraciones:

1. Abrir pgAdmin 4.
2. Conectarse al servidor PostgreSQL.
3. Crear una nueva base de datos llamada:

```text
crm_db
```

4. Verificar que la contraseña del usuario `postgres` coincida con el valor configurado en el archivo `.env`.

---

## Instalar GTK para WeasyPrint

Si aparece un error relacionado con:

```text
libgobject-2.0-0
```

instalar GTK:

```powershell
winget install --id tschoonj.GTKForWindows -e
```

Después de la instalación, reiniciar la terminal.

---

## Ejecutar Migraciones

Desde la carpeta `backend`:

```powershell
uv run python manage.py migrate
```

---

## Crear un Superusuario (Opcional)

```powershell
uv run python manage.py createsuperuser
```

---

## Ejecutar el Servidor

```powershell
uv run python manage.py runserver
```

El backend estará disponible en:

```text
http://127.0.0.1:8000
```

Panel de administración:

```text
http://127.0.0.1:8000/admin
```

---

# Resumen de Comandos

## Frontend

```bash
cd frontend
pnpm install
pnpm run dev
```

## Backend

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv --version

copy .env.example .env

winget install --id tschoonj.GTKForWindows -e

uv run python manage.py migrate

uv run python manage.py createsuperuser

uv run python manage.py runserver
```
