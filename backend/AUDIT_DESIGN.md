# Diseño del Sistema de Auditoría (#86)

## 1. Justificación técnica
Para optimizar el control de datos sin afectar el rendimiento, se implementó un sistema de auditoría automatizado mediante la librería `django-simple-history`. El alcance inicial cubre los módulos críticos de **Leads, Contacts, Accounts y Opportunity**, ya que gestionan el flujo financiero y comercial principal del CRM.

## 2. ¿Cómo se hizo? (Componentes clave)
La integración se estructuró de manera modular modificando los siguientes archivos esenciales del proyecto:
* **`backend/crm/settings.py`**: Se activó la aplicación `simple_history` y su middleware global junto al componente `crum` para capturar sesiones JWT.
* **Módulos de datos (ej. `leads/models.py`)**: Se inyectó la propiedad `history = HistoricalRecords()` para activar la creación de tablas espejo automatizadas.
* **`backend/common/views/audit_views.py`**: Se diseñó la lógica independiente `GlobalAuditListView` para mezclar cronológicamente los registros históricos.
* **`frontend/src/routes/(app)/auditoria/`**: Se construyó la interfaz en SvelteKit con componentes reactivos y filtros dinámicos por módulo para los administradores.

## 3. ¿Cómo funciona el flujo de datos?
1. **Acción del usuario**: Un operador edita o elimina un registro desde la interfaz visual del CRM.
2. **Intercepción del Backend**: La petición HTTP es evaluada por `HistoryRequestMiddleware`, el cual extrae de forma transparente la identidad del usuario autenticado.
3. **Persistencia dual**: Django guarda el cambio en la tabla activa del módulo e, inmediatamente, la librería toma una "fotografía" del estado anterior y nuevo de los datos.
4. **Almacenamiento seguro**: Toda la información (fecha, autor, tipo de operación `+`, `~`, `-` y campos modificados) se inserta de forma atómica en la tabla histórica de auditoría.
