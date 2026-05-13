# Stack Tecnológico

## Introducción

BottleCRM es una plataforma CRM open source desarrollada bajo una arquitectura moderna cliente-servidor. El proyecto utiliza tecnologías ampliamente adoptadas en la industria para garantizar escalabilidad, mantenibilidad y seguridad.

---

# Backend

## Python 3.10+

Python es un lenguaje de programación de alto nivel ampliamente utilizado en desarrollo web, automatización, inteligencia artificial y ciencia de datos.

### Vigencia en la industria
- Alta demanda laboral.
- Amplio ecosistema de librerías.
- Desarrollo rápido y mantenible.
- Muy utilizado en startups y empresas tecnológicas.

### Uso en el proyecto
BottleCRM utiliza Python como lenguaje principal para el backend y lógica de negocio.

---

## Django 5.x

Django es un framework web basado en Python que sigue el patrón MTV (Model-Template-View).

### Características principales
- Seguridad integrada.
- ORM robusto.
- Escalabilidad.
- Desarrollo rápido.
- Arquitectura modular.

### Vigencia en la industria
Django continúa siendo utilizado en aplicaciones empresariales, plataformas SaaS y sistemas escalables debido a su estabilidad y productividad.

### Uso en el proyecto
BottleCRM implementa Django junto con Django REST Framework para exponer servicios API REST.

---

## Django REST Framework (DRF)

Framework especializado para construcción de APIs REST sobre Django.

### Funcionalidades
- Serialización de datos.
- Autenticación JWT.
- Permisos y seguridad.
- Documentación de APIs.

### Uso en el proyecto
Permite la comunicación entre el frontend SvelteKit y el backend.

---

## PostgreSQL

Sistema de gestión de bases de datos relacional open source.

### Características principales
- Alto rendimiento.
- Soporte ACID.
- Escalabilidad.
- Seguridad avanzada.

### Vigencia en la industria
PostgreSQL es ampliamente utilizado en sistemas empresariales modernos y servicios cloud.

### Uso en el proyecto
BottleCRM utiliza PostgreSQL con Row-Level Security (RLS) para implementar aislamiento seguro entre organizaciones.

---

## Redis

Base de datos en memoria utilizada para caching y mensajería.

### Uso en el proyecto
- Broker de Celery.
- Caché.
- Procesamiento asíncrono.

---

## Celery

Herramienta de procesamiento de tareas asíncronas.

### Uso en el proyecto
Permite ejecutar procesos en segundo plano como:
- envío de correos,
- procesamiento de tareas,
- automatización de eventos.

---

# Frontend

## SvelteKit 2.x

Framework moderno para desarrollo frontend basado en Svelte.

### Características
- Alto rendimiento.
- Renderizado eficiente.
- Arquitectura moderna.
- Experiencia fluida de usuario.

### Vigencia en la industria
SvelteKit está creciendo rápidamente debido a su simplicidad y rendimiento frente a frameworks tradicionales.

### Uso en el proyecto
Construcción de toda la interfaz gráfica del CRM.

---

## TailwindCSS

Framework CSS utility-first.

### Beneficios
- Desarrollo rápido.
- Diseño responsivo.
- Código reutilizable.
- Menor cantidad de CSS personalizado.

---

# Infraestructura y DevOps

## Docker

Plataforma de contenedores para despliegue consistente.

### Uso en el proyecto
BottleCRM utiliza Docker Compose para levantar:
- Backend
- Frontend
- PostgreSQL
- Redis
- Celery

---

## JWT Authentication

Sistema de autenticación basado en tokens.

### Beneficios
- Seguridad.
- Escalabilidad.
- Integración sencilla con APIs REST.

---

# Conclusión

El stack tecnológico seleccionado en BottleCRM representa una arquitectura moderna ampliamente utilizada en la industria del software. La combinación de Django, PostgreSQL y SvelteKit permite desarrollar aplicaciones escalables, seguras y mantenibles, alineadas con prácticas actuales de desarrollo web y DevOps.