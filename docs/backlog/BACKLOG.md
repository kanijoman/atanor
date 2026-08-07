# BACKLOG

# Información del documento

| Campo                | Valor               |
| -------------------- | ------------------- |
| Proyecto             | Atanor              |
| Documento            | BACKLOG             |
| Estado del documento | 🟢 Activo           |
| Versión              | 0.1                 |
| Última actualización | 2026-08-07          |
| Hito activo          | Hito 1 · Foundation |

---

> **Documento vivo**
>
> Este documento recoge el trabajo pendiente del proyecto Atanor.
>
> Las tareas se organizan por hitos y épicas, siguiendo el roadmap del proyecto.
> Únicamente el hito activo se detalla a nivel de tareas. Los hitos futuros se refinan conforme pasan a estar activos.

---

# Estado del backlog

| Estado      | Cantidad |
| ----------- | -------: |
| Pendientes  |       19 |
| En progreso |        0 |
| Completadas |        3 |
| Canceladas  |        2 |
| Bloqueadas  |        0 |

---

# Convenciones

# Gestión del backlog

El backlog es una herramienta de planificación viva que refleja el estado y la dirección del proyecto, pero no constituye una especificación técnica detallada.

## Principios

- Los identificadores de las tareas son únicos e inmutables. Nunca se renumeran.
- Una vez que una tarea pasa a estado **En progreso**, su definición se considera congelada. Los detalles de implementación se documentan mediante los commits asociados.
- Si durante la implementación se detecta trabajo adicional, este deberá planificarse como una nueva tarea, evitando ampliar el alcance de la tarea en curso.
- Una tarea puede cancelarse si deja de aportar valor al proyecto o si se considera prematura. En ese caso, no se reutilizará su identificador.
- Si en el futuro el trabajo vuelve a ser necesario, se creará una nueva tarea con un nuevo identificador.
- El historial de Git constituye el registro técnico del proyecto; el backlog refleja únicamente la planificación y el estado de las tareas.

## Identificador

Todas las tareas se identifican mediante un código único.

```
AT-001
AT-002
AT-003
...
```

---

## Estados

* ⬜ Pendiente
* 🟡 En progreso
* ✅ Completada
* ❌ Cancelada
* ⛔ Bloqueada

---

## Prioridades

* 🔴 Alta
* 🟠 Media
* 🟡 Baja

---

# Hito 1 · Foundation

**Objetivo**

Disponer de una plataforma base completamente operativa sobre la que desarrollar el resto del producto.

---

## Épica A · Infraestructura

| ID     | Tarea                                       | Prioridad | Estado |
| ------ | ------------------------------------------- | --------- | ------ |
| AT-001 | Crear la estructura inicial del repositorio | 🔴 Alta   | ✅ |
| AT-002 | Inicializar el repositorio backend          | 🔴 Alta   | ✅      |
| AT-003 | Inicializar el repositorio frontend         | 🔴 Alta   | ✅      |
| AT-004 | Configurar Docker Compose inicial           | 🔴 Alta   | ❌      |
| AT-005 | Configurar variables de entorno             | 🔴 Alta   | ❌      |

---

## Épica B · Backend

| ID     | Tarea                               | Prioridad | Estado |
| ------ | ----------------------------------- | --------- | ------ |
| AT-010 | Inicializar proyecto FastAPI        | 🔴 Alta   | ⬜      |
| AT-011 | Configurar sistema de configuración | 🔴 Alta   | ⬜      |
| AT-012 | Implementar logging                 | 🟠 Media  | ⬜      |
| AT-013 | Implementar endpoint `/health`      | 🔴 Alta   | ⬜      |
| AT-014 | Implementar endpoint `/version`     | 🟠 Media  | ⬜      |

---

## Épica C · Persistencia

| ID     | Tarea                                      | Prioridad | Estado |
| ------ | ------------------------------------------ | --------- | ------ |
| AT-020 | Configurar PostgreSQL                      | 🔴 Alta   | ⬜      |
| AT-021 | Integrar SQLAlchemy                        | 🔴 Alta   | ⬜      |
| AT-022 | Configurar Alembic                         | 🔴 Alta   | ⬜      |
| AT-023 | Crear la primera migración                 | 🔴 Alta   | ⬜      |
| AT-024 | Implementar la primera entidad del dominio | 🔴 Alta   | ⬜      |

---

## Épica D · Frontend

| ID     | Tarea                                   | Prioridad | Estado |
| ------ | --------------------------------------- | --------- | ------ |
| AT-030 | Inicializar proyecto React + TypeScript | 🔴 Alta   | ⬜      |
| AT-031 | Configurar Tailwind CSS                 | 🟠 Media  | ⬜      |
| AT-032 | Crear la página principal               | 🔴 Alta   | ⬜      |
| AT-033 | Configurar cliente HTTP                 | 🟠 Media  | ⬜      |

---

## Épica E · Calidad

| ID     | Tarea                        | Prioridad | Estado |
| ------ | ---------------------------- | --------- | ------ |
| AT-040 | Configurar Ruff              | 🔴 Alta   | ⬜      |
| AT-041 | Configurar Pytest            | 🔴 Alta   | ⬜      |
| AT-042 | Configurar ESLint y Prettier | 🟠 Media  | ⬜      |
| AT-043 | Configurar GitHub Actions    | 🔴 Alta   | ⬜      |

---

## Épica F · Vertical Slice

| ID     | Tarea                                | Prioridad | Estado |
| ------ | ------------------------------------ | --------- | ------ |
| AT-050 | Diseñar la entidad Documento         | 🔴 Alta   | ⬜      |
| AT-051 | Implementar CRUD de Documento        | 🔴 Alta   | ⬜      |
| AT-052 | Persistir Documento en base de datos | 🔴 Alta   | ⬜      |
| AT-053 | Exponer la API de Documento          | 🔴 Alta   | ⬜      |
| AT-054 | Integrar Frontend ↔ Backend          | 🔴 Alta   | ⬜      |
| AT-055 | Validar el flujo end-to-end          | 🔴 Alta   | ⬜      |

---

# Hito 2 · Ingesta documental

## Épicas previstas

* Carga de documentos.
* Extracción de texto.
* Normalización documental.
* Persistencia documental.

---

# Hito 3 · Recuperación del conocimiento

## Épicas previstas

* Indexación.
* Búsqueda.
* Recuperación semántica.
* Ranking de resultados.

---

# Hito 4 · Asistente jurídico

## Épicas previstas

* Integración de LLM.
* Arquitectura RAG.
* Gestión de citas y referencias.
* Conversación contextual.

---

# Hito 5 · Plataforma de aprendizaje

## Épicas previstas

* Gestión de temarios.
* Planificador de estudio.
* Generación de tests.
* Seguimiento del progreso.
* Repaso espaciado.

---

# Hito 6 · Escalabilidad

## Épicas previstas

* Autenticación.
* Gestión de usuarios.
* Autorización y permisos.
* Monitorización.
* Despliegue en producción.

---

# Icebox

Ideas que no forman parte del MVP pero que pueden aportar valor en futuras iteraciones.

* Visualización del grafo de conocimiento.
* Aplicación móvil.
* Importación automática desde el BOE.
* Sincronización entre dispositivos.
* API pública.
* Soporte multiidioma.
