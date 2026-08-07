# ROADMAP

> **Documento vivo**
>
> Este documento define la planificación y el estado de ejecución del proyecto Atanor.
> Debe mantenerse actualizado durante todo el ciclo de vida del proyecto y reflejar fielmente el estado real del desarrollo.

---

# Información del proyecto

| Campo                | Valor                                    |
| -------------------- | ---------------------------------------- |
| Proyecto             | Atanor                                   |
| Estado               | 🟢 En desarrollo                         |
| Versión del roadmap  | 0.1                                      |
| Última actualización | 2026-08-07                               |
| Sprint activo        | Sprint 0.1 – Modelo de Conocimiento      |
| Próximo objetivo     | Definir el modelo conceptual del dominio |

---

# Visión del MVP

El objetivo del MVP es desarrollar un asistente inteligente para la preparación de oposiciones de la Administración General del Estado.

El sistema deberá ser capaz de:

* Gestionar conocimiento jurídico.
* Organizar temarios oficiales.
* Relacionar el contenido con fuentes oficiales.
* Guiar el proceso de aprendizaje del opositor.
* Generar contenido de estudio fundamentado.

Todo el desarrollo debe orientarse a este objetivo.

---

# Roadmap general

| Hito   | Objetivo                 | Prioridad | Estado      | Progreso |
| ------ | ------------------------ | --------- | ----------- | -------- |
| Hito 0 | Fundamentos              | 🔴 Alta   | 🟡 En curso | 10%      |
| Hito 1 | Gestión del conocimiento | 🔴 Alta   | ⚪ Pendiente | 0%       |
| Hito 2 | Integración de fuentes   | 🟠 Media  | ⚪ Pendiente | 0%       |
| Hito 3 | Motor de aprendizaje     | 🔴 Alta   | ⚪ Pendiente | 0%       |
| Hito 4 | Guiado inteligente       | 🔴 Alta   | ⚪ Pendiente | 0%       |
| Hito 5 | Analítica                | 🟡 Baja   | ⚪ Pendiente | 0%       |
| Hito 6 | Escalabilidad            | 🟡 Baja   | ⚪ Pendiente | 0%       |

---

# Estado de ejecución

| Sprint                              | Prioridad | Estado      | Progreso |
| ----------------------------------- | --------- | ----------- | -------- |
| Sprint 0.1 · Modelo de Conocimiento | 🔴 Alta   | 🟡 En curso | 0%       |

---

# Hito 0 · Fundamentos

## Objetivo

Construir una base técnica y conceptual sólida que permita evolucionar Atanor durante los próximos años sin necesidad de rediseñar la arquitectura.

Este hito no persigue funcionalidades para el usuario final, sino definir correctamente el dominio del problema.

---

# Sprint 0.1 · Modelo de Conocimiento

## Objetivo

Diseñar el modelo conceptual del conocimiento que utilizará Atanor.

Antes de implementar funcionalidades, bases de datos o IA, el sistema debe comprender correctamente cómo se estructura el conocimiento jurídico y académico.

---

## Prioridad

🔴 Alta

---

## Estado

🟡 En curso

---

## Progreso

**0 %**

---

## Tareas

### Modelo conceptual

* [ ] Definir las entidades principales del dominio.
* [ ] Definir relaciones entre entidades.
* [ ] Definir cardinalidades.
* [ ] Establecer reglas de negocio.

### Modelo de persistencia

* [ ] Diseñar el modelo relacional.
* [ ] Diseñar relaciones muchos-a-muchos.
* [ ] Definir claves primarias y foráneas.

### Implementación

* [ ] Crear entidades mediante SQLAlchemy.
* [ ] Generar el esquema inicial de base de datos.
* [ ] Validar la integridad del modelo.

---

## Entidades previstas

* Documento
* Capítulo
* Artículo
* Fuente
* Tema
* Epígrafe
* Pregunta
* Fragmento *(entidad prevista para futuras funcionalidades de recuperación semántica y RAG)*

---

## Entregables

* Modelo conceptual del dominio.
* Diagrama de entidades.
* Modelo relacional.
* Esquema inicial de base de datos.
* Implementación inicial del dominio.

---

## Criterios de aceptación

El sprint se considerará completado cuando:

* [ ] El modelo represente correctamente un temario oficial.
* [ ] Permita relacionar un mismo tema con múltiples fuentes.
* [ ] Permita reutilizar una fuente en distintos temas.
* [ ] El modelo pueda evolucionar sin modificaciones estructurales importantes.
* [ ] Existan pruebas básicas de validación.

---

# Próximos hitos

## Hito 1 · Gestión del Conocimiento

**Objetivo**

Gestionar documentos, temas y estructura del conocimiento.

---

## Hito 2 · Integración de Fuentes

**Objetivo**

Importar conocimiento desde fuentes oficiales y temarios.

---

## Hito 3 · Motor de Aprendizaje

**Objetivo**

Gestionar el progreso del estudiante y la trazabilidad del conocimiento.

---

## Hito 4 · Guiado Inteligente

**Objetivo**

Incorporar funcionalidades inteligentes para asistir el aprendizaje.

---

## Hito 5 · Analítica

**Objetivo**

Proporcionar métricas y recomendaciones personalizadas.

---

## Hito 6 · Escalabilidad

**Objetivo**

Preparar Atanor para un entorno multiusuario y despliegues en producción.

---

# Definition of Done

Todo sprint deberá cumplir los siguientes requisitos antes de darse por finalizado.

* [ ] Objetivos del sprint completados.
* [ ] Código implementado.
* [ ] Tests básicos superados.
* [ ] Documentación actualizada.
* [ ] Sin incidencias críticas abiertas.
* [ ] Integración en la rama principal.

---

# Decisiones de arquitectura

| Fecha      | Decisión                                                                                 | Motivo                                                             |
| ---------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 2026-08-06 | Python como lenguaje principal                                                           | Máxima productividad y ecosistema de IA.                           |
| 2026-08-06 | Arquitectura orientada al dominio                                                        | El modelo de conocimiento será el núcleo de Atanor.                |
| 2026-08-06 | SQLAlchemy como ORM inicial                                                              | Flexibilidad y control sobre el modelo relacional.                 |
| 2026-08-06 | Desarrollo iterativo por hitos y sprints                                                 | Reducir riesgo y validar continuamente la arquitectura.            |
| 2026-08-07 | El MVP se centrará exclusivamente en oposiciones de la Administración General del Estado | Mantener un alcance reducido y maximizar la probabilidad de éxito. |

---

# Decisiones pendientes

* [ ] SQLAlchemy vs SQLModel.
* [ ] SQLite o PostgreSQL durante la beta.
* [ ] Estrategia de almacenamiento vectorial.
* [ ] Arquitectura multi-provider para LLM.
* [ ] Sistema de versionado documental.
* [ ] Estrategia de actualización automática de normativa.

---

# Riesgos conocidos

* Evolución del modelo de dominio durante las primeras iteraciones.
* Cambios en la normativa jurídica.
* Dependencia de proveedores de modelos LLM.
* Complejidad creciente del grafo de conocimiento.

---

# Métricas del proyecto

| Indicador                | Valor      |
| ------------------------ | ---------- |
| Hitos completados        | 0 / 7      |
| Sprint activo            | Sprint 0.1 |
| Progreso global estimado | 2 %        |
| Bloqueadores             | Ninguno    |

---

# Changelog

## 2026-08-07

* Creación del ROADMAP.md.
* Definición del Hito 0.
* Definición del Sprint 0.1.
* Incorporación de métricas de progreso.
* Registro inicial de decisiones de arquitectura.
