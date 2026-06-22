# Guía de Instalación y Configuración del Sistema

## 1. Descripción
Esta guía detalla el procedimiento completo para desplegar el proyecto en un entorno local o de pruebas desde cero. Su objetivo es facilitar la incorporación de nuevos miembros al equipo, asegurar la replicación exacta de entornos y minimizar los tiempos de configuración y resolución de problemas.

## 2. Requisitos Previos y Versiones
Asegúrate de contar con las siguientes especificaciones y herramientas instaladas en tu máquina anfitriona:

### Requisitos de Hardware (Mínimo recomendado)
- **Procesador:** 4 Núcleos (x86_64 o ARM64 como Apple Silicon).
- **Memoria RAM:** 8 GB o superior.
- **Espacio en disco:** 10 GB de espacio libre.

### Requisitos de Software y Versiones
- **Sistema Operativo:** Linux, macOS o Windows (con WSL2 habilitado).
- **Git:** Versión 2.30 o superior.
- **Docker:** Versión 20.10 o superior.
- **Docker Compose:** Versión 2.20 o superior.
- **Gestores internos:** `uv` (Python/Django) y `pnpm` (Node.js/Frontend) empaquetados en los contenedores.

---

## 3. Clonar el Repositorio
Abre una terminal y ejecuta los siguientes comandos para clonar el repositorio del proyecto e ingresar a la carpeta raíz:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO_DEL_PROYECTO>
```

---

## 4. Cambios Obligatorios en Archivos (Configuración Inicial)
Antes de construir los contenedores, debes aplicar de manera exacta las siguientes modificaciones en el código fuente:

1. **Docker/backend -> entrypoint.sh**:
   - Cambiar el formato de los saltos de línea de CRLF a **LF** (este ajuste se realiza en la esquina inferior derecha de editores de código como VS Code).

2. **frontend/Dockerfile**:
   - Insertar en las líneas 10 y 11 las siguientes instrucciones de entorno e instalación:
```dockerfile
     ENV CI=true
     RUN pnpm install --no-frozen-lockfile --ignore-scripts
     ```

3. **.dockerignore**:
   - Añadir al final del archivo para evitar la copia de entornos virtuales locales:
```text
     backend/.venv
     backend/.venv/
     ```

4. **.env.docker**:
   - Asegurar que la URL del API de Django para el Frontend apunte al contenedor correspondiente:
```env
     # Frontend
     PUBLIC_DJANGO_API_URL=http://backend:8000
     ```

5. **backend/common -> tasks.py**:
   - Insertar exactamente debajo de la línea 84 la impresión en consola para el token de autenticación:
```python
     print(f"\n\n-------- AQUÍ ESTÁ TU ENLACE MÁGICO: {magic_link_url}\n\n")
     ```

---

## 5. Pasos en la Consola (Despliegue del Entorno)
Ejecuta de forma secuencial los siguientes comandos en la terminal desde la raíz del proyecto:

1. **Copiar el archivo de entorno base para el backend:**
```bash
   cp backend/.env.example backend/.env
   ```

2. **Copiar el archivo de configuración de entorno para Docker:**
```bash
   cp .env.docker .env.docker.local
   ```

3. **Sincronizar y descargar librerías (Django, Celery, etc.):**
```bash
   docker compose run --rm backend uv sync
   ```

4. **Construir imágenes y levantar el proyecto por primera vez:**
```bash
   docker compose up --build
   ```
   *(Nota: Mantén esta pestaña de la terminal abierta para observar los logs de ejecución).*

5. **Inyectar datos de prueba (Seed Data):**
   Abre una **nueva pestaña o ventana de la terminal**, sitúate en la raíz del proyecto y ejecuta el comando para poblar la base de datos con el administrador de prueba:
```bash
   docker compose exec backend python manage.py seed_data --email admin@example.com
   ```

6. **Apagado y Encendido Diario:**
   Para detener los contenedores, presiona `Ctrl + C` en la terminal de los logs. Para volver a encender el proyecto en el día a día sin reinstalar nada, ejecuta:
```bash
   docker compose up
   ```

---

## 6. Validación del Funcionamiento
Para constatar que el sistema se ha desplegado correctamente, sigue este protocolo de pruebas:
1. Abre tu navegador web e ingresa a la URL local del Frontend (ej. `http://localhost:3000` o el puerto configurado en tu entorno).
2. En la pantalla de inicio de sesión, introduce el correo electrónico de prueba: `admin@example.com`.
3. Revisa la terminal donde se están ejecutando los logs de `docker compose up`.
4. Verifica que se haya impreso la línea configurada en las tareas:
   `-------- AQUÍ ESTÁ TU ENLACE MÁGICO: http://localhost:8000/auth/...`
5. Copia dicho enlace, pégalo en el navegador y confirma que accedes al sistema de forma exitosa.

---

## 7. Solución de Errores Frecuentes (Troubleshooting)

### Error de formato en script de entrada (`standard_init_linux.go` o caracteres `\r`)
- **Síntoma:** El contenedor `backend` falla de inmediato o arroja errores de comandos no encontrados.
- **Causa:** El archivo `Docker/backend/entrypoint.sh` posee formato de fin de línea de Windows (CRLF).
- **Solución:** Abre el archivo en tu editor, cambia el formato a **LF** en la barra de estado inferior, guarda el archivo y vuelve a ejecutar `docker compose up --build`.

### Dependencias desactualizadas o fallos en el Frontend
- **Síntoma:** El build del frontend falla por conflictos de paquetes de nodos.
- **Solución:** Verifica que las líneas agregadas en el `frontend/Dockerfile` (`--no-frozen-lockfile`) estén presentes para forzar la instalación correcta ignorando bloqueos de versiones locales estrictas.
````</NOMBRE_DEL_DIRECTORIO_DEL_PROYECTO></URL_DEL_REPOSITORIO>
