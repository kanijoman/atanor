# ROADMAP

# Información del documento

| Campo                 | Valor                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------- |
| Proyecto              | Atanor                                                                                   |
| Documento             | ROADMAP                                                                                  |
| Estado del documento  | 🟢 Activo                                                                                |
| Versión del documento | 0.2                                                                                      |
| Última actualización  | 2026-08-07                                                                               |
| Hito activo           | Hito 1 · Foundation                                                                      |
| Próximo objetivo      | Disponer de una plataforma base completamente operativa para el desarrollo del producto. |

---

> **Documento vivo**
>
> Este documento define la planificación estratégica y el estado de evolución del proyecto Atanor.
> Debe mantenerse actualizado durante todo el ciclo de vida del proyecto y reflejar fielmente el estado real del desarrollo.
> El detalle de las tareas se mantiene en el **BACKLOG**, mientras que este documento describe la evolución del producto mediante hitos.

---

# Información del proyecto

| Campo                | Valor                                                                  |
| -------------------- | ---------------------------------------------------------------------- |
| Proyecto             | Atanor                                                                 |
| Estado               | 🟢 En desarrollo                                                       |
| Versión del roadmap  | 0.2                                                                    |
| Última actualización | 2026-08-07                                                             |
| Hito activo          | Hito 1 · Foundation                                                    |
| Próximo objetivo     | Construir la infraestructura técnica sobre la que evolucionará Atanor. |

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

| Hito   | Objetivo                      | Prioridad | Estado       | Progreso |
| ------ | ----------------------------- | --------- | ------------ | -------- |
| Hito 0 | Fundamentos                   | 🔴 Alta   | ✅ Completado | 100 %    |
| Hito 1 | Foundation                    | 🔴 Alta   | 🟡 En curso  | 0 %      |
| Hito 2 | Ingesta documental            | 🔴 Alta   | ⚪ Pendiente  | 0 %      |
| Hito 3 | Recuperación del conocimiento | 🔴 Alta   | ⚪ Pendiente  | 0 %      |
| Hito 4 | Asistente jurídico            | 🔴 Alta   | ⚪ Pendiente  | 0 %      |
| Hito 5 | Plataforma de aprendizaje     | 🔴 Alta   | ⚪ Pendiente  | 0 %      |
| Hito 6 | Escalabilidad                 | 🟡 Media  | ⚪ Pendiente  | 0 %      |

---

# Estado de ejecución

## Hito activo

**Hito 1 · Foundation**

## Estado

🟡 En curso

## Progreso

**0 %**

---

# Hito 0 · Fundamentos

## Objetivo

Construir una base conceptual, organizativa y arquitectónica sólida que permita desarrollar Atanor de forma iterativa, manteniendo una visión clara del producto y reduciendo el riesgo de rediseños futuros.

---

## Estado

✅ Completado

---

## Resultados obtenidos

* Definición de la visión y alcance del producto.
* Diseño de la arquitectura inicial.
* Definición del roadmap estratégico.
* Establecimiento de las convenciones de desarrollo.
* Creación del README del proyecto.
* Consolidación de la documentación fundacional.

---

## Entregables

* Visión del producto.
* Arquitectura inicial.
* Roadmap.
* Convenciones de desarrollo.
* README.
* Documentación técnica inicial.

---

# Hito 1 · Foundation

## Objetivo

Construir la infraestructura técnica mínima que permita desarrollar funcionalidades de forma rápida, segura y mantenible durante el resto del proyecto.

---

## Estado

🟡 En curso

---

## Progreso

**0 %**

---

## Líneas de trabajo

### Infraestructura

* Definir la estructura del repositorio.
* Configurar el entorno de desarrollo.
* Configurar Git y la estrategia de ramas.
* Configurar Docker.

### Backend

* Inicializar FastAPI.
* Configurar el sistema de configuración mediante variables de entorno.
* Implementar el sistema de logging.
* Crear los endpoints básicos del sistema.

### Persistencia

* Configurar PostgreSQL.
* Integrar SQLAlchemy.
* Configurar Alembic.
* Generar la primera migración.

### Frontend

* Inicializar React + TypeScript.
* Configurar Vite.
* Configurar Tailwind CSS.
* Crear la primera interfaz del proyecto.

### Calidad

* Configurar Ruff.
* Configurar MyPy.
* Configurar Pytest.
* Configurar ESLint y Prettier.
* Configurar GitHub Actions.

### Vertical Slice

* Implementar la primera entidad del dominio.
* Exponer un CRUD básico.
* Validar el flujo Frontend → Backend → Base de datos.

---

## Entregables

* Backend operativo.
* Frontend operativo.
* Base de datos funcional.
* Docker Compose.
* Pipeline de integración continua.
* Primera entidad persistida.
* Vertical Slice completamente funcional.

---

## Criterios de aceptación

El hito se considerará completado cuando:

* [ ] El proyecto pueda ejecutarse completamente mediante Docker Compose.
* [ ] Backend y frontend se comuniquen correctamente.
* [ ] Exista una primera migración funcional.
* [ ] La integración continua valide lint, tests y build.
* [ ] Exista una primera entidad persistida en la base de datos.
* [ ] La arquitectura esté preparada para comenzar el desarrollo funcional.

---

# Próximos hitos

## Hito 2 · Ingesta documental

**Objetivo**

Permitir la incorporación, almacenamiento y procesamiento de documentos jurídicos y temarios oficiales.

---

## Hito 3 · Recuperación del conocimiento

**Objetivo**

Implementar mecanismos de búsqueda, indexación y recuperación eficiente de la información.

---

## Hito 4 · Asistente jurídico

**Objetivo**

Incorporar un asistente inteligente capaz de responder utilizando el conocimiento almacenado.

---

## Hito 5 · Plataforma de aprendizaje

**Objetivo**

Desarrollar las funcionalidades específicas para la preparación de oposiciones: planificación, estudio, evaluación y seguimiento.

---

## Hito 6 · Escalabilidad

**Objetivo**

Preparar Atanor para despliegues en producción, soporte multiusuario y crecimiento del producto.

---

# Definition of Done

Todo hito deberá cumplir los siguientes requisitos antes de darse por finalizado.

* [ ] Objetivos del hito completados.
* [ ] Código implementado.
* [ ] Tests básicos superados.
* [ ] Documentación actualizada.
* [ ] Sin incidencias críticas abiertas.
* [ ] Integración en la rama principal.

---

# Decisiones de arquitectura

| Fecha      | Decisión                                                                                 | Motivo                                                                        |
| ---------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 2026-08-06 | Python como lenguaje principal                                                           | Máxima productividad y ecosistema de IA.                                      |
| 2026-08-06 | Arquitectura orientada al dominio                                                        | El modelo de conocimiento será el núcleo de Atanor.                           |
| 2026-08-06 | SQLAlchemy como ORM inicial                                                              | Flexibilidad y control sobre el modelo relacional.                            |
| 2026-08-06 | Desarrollo iterativo por hitos                                                           | Reducir riesgo y validar continuamente la arquitectura.                       |
| 2026-08-07 | El MVP se centrará exclusivamente en oposiciones de la Administración General del Estado | Mantener un alcance reducido y maximizar la probabilidad de éxito.            |
| 2026-08-07 | Eliminación de sprints temporales                                                        | Adaptar la planificación a un desarrollo iterativo propio de un side project. |

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

| Indicador                | Valor               |
| ------------------------ | ------------------- |
| Hitos completados        | 1 / 7               |
| Hito activo              | Hito 1 · Foundation |
| Progreso global estimado | 12 %                |
| Bloqueadores             | Ninguno             |

---

# Changelog

## 2026-08-07

* Creación del ROADMAP.md.
* Definición del Hito 0.
* Definición del roadmap inicial.
* Incorporación de métricas de progreso.
* Registro inicial de decisiones de arquitectura.

## 2026-08-07 (Actualización)

* Finalizado el Hito 0 · Fundamentos.
* Reorganización del roadmap en torno a hitos de producto.
* Eliminado el concepto de sprint como unidad temporal.
* Inicio del Hito 1 · Foundation.
* Separación conceptual entre ROADMAP y BACKLOG.
