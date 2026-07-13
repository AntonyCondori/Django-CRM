# Diseño del Sistema de Auditoría (#86)

## 1. ¿Qué vamos a auditar?
Para empezar de forma rápida y enfocada, auditaremos la tabla de **Leads** (Clientes Potenciales). Es la parte más importante del CRM porque maneja los datos de las ventas, los estados del negocio y qué asesor tiene asignado cada cliente.

## 2. Acciones que se van a registrar
El sistema guardará un registro de forma automática cada vez que pase una de estas tres cosas con un Lead:
* **Creación (+):** Cuando se registra un Lead nuevo.
* **Modificación (~):** Cuando se edita cualquier dato (Guarda el cambio y el valor anterior).
* **Eliminación (-):** Cuando alguien borra un Lead (Así no se pierde el rastro de la información).

## 3. Datos que se van a guardar (Estructura)
Por cada cambio que ocurra, la base de datos creará un registro de auditoría en una tabla espejo con los siguientes datos:
* **ID del Historial:** Un número único para identificar ese registro de auditoría.
* **Fecha y Hora:** El momento exacto en el que se hizo el cambio.
* **Usuario:** Quién fue la persona logueada en el CRM que hizo la acción.
* **Tipo de Acción:** Si fue una creación, edición o eliminación.
* **Copia de los datos:** Una "fotografía" de cómo estaba el Lead en ese preciso instante.

## 4. ¿Cómo funciona el flujo?
1. El usuario hace un cambio en el CRM (por ejemplo, edita el teléfono de un Lead).
2. La aplicación recibe la petición y el "Middleware" (el vigilante del backend) identifica automáticamente qué usuario está conectado.
3. Django guarda el cambio normal en la tabla de Leads.
4. Al mismo tiempo, la librería que instalamos toma los datos del usuario, el cambio realizado, la hora, y lo guarda todo en la tabla de historial sin que el usuario note ninguna lentitud.
