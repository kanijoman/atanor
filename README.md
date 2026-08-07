# Atanor

> **Un asistente inteligente para la preparación de oposiciones.**

Atanor es una plataforma diseñada para ayudar a opositores a estudiar de forma más eficiente mediante la organización del conocimiento, el análisis de fuentes oficiales y la aplicación de inteligencia artificial como herramienta de apoyo al aprendizaje.

El proyecto nace con un objetivo muy concreto: construir un asistente capaz de preparar oposiciones de la Administración General del Estado utilizando exclusivamente información fundamentada y trazable.

Aunque el primer MVP está centrado en oposiciones, la arquitectura está diseñada para evolucionar hacia una plataforma de gestión del conocimiento aplicable a otros ámbitos.

---

## Objetivos

El MVP de Atanor debe ser capaz de:

* Gestionar temarios y documentación oficial.
* Organizar el conocimiento en una estructura coherente y reutilizable.
* Relacionar cada contenido con sus fuentes oficiales.
* Ayudar al opositor durante el proceso de estudio.
* Generar preguntas, explicaciones y material de aprendizaje fundamentado.
* Realizar un seguimiento del progreso del estudiante.

---

## Principios del proyecto

Atanor se desarrolla siguiendo una serie de principios fundamentales:

* **El conocimiento es el núcleo del sistema.**
* **La IA es una herramienta, no el producto.**
* **Toda respuesta debe ser trazable hasta una fuente verificable.**
* **La arquitectura debe priorizar la mantenibilidad sobre la complejidad.**
* **El desarrollo será iterativo, incremental y orientado al dominio.**

---

## Estado del proyecto

Actualmente el proyecto se encuentra en la fase de definición de la arquitectura y del modelo de conocimiento.

El desarrollo activo corresponde al:

> **Hito 0 · Fundamentos**

En esta etapa se está definiendo el dominio que permitirá representar el conocimiento jurídico y académico dentro de Atanor antes de comenzar el desarrollo de funcionalidades.

---

## Documentación

La documentación principal del proyecto se encuentra en los siguientes archivos:

| Documento          | Descripción                                                                           |
| ------------------ | ------------------------------------------------------------------------------------- |
| **FOUNDATIONS.md** | Visión del proyecto, principios de diseño y decisiones arquitectónicas fundamentales. |
| **ROADMAP.md**     | Estado del proyecto, planificación, hitos y progreso del desarrollo.                  |

---

## Filosofía de desarrollo

Atanor adopta un enfoque **Domain-Driven Design (DDD) ligero**, donde el modelo de conocimiento constituye el centro de toda la arquitectura.

Antes de implementar nuevas funcionalidades se define el dominio que representan, permitiendo construir una base sólida sobre la que evolucionar sin necesidad de rediseños constantes.

Cada iteración busca entregar un incremento funcional manteniendo una arquitectura limpia, desacoplada y fácilmente extensible.

---

## Tecnologías previstas

La implementación inicial utilizará:

* Python
* SQLAlchemy
* SQLite (MVP)
* FastAPI
* Pydantic
* Pytest

La arquitectura permitirá incorporar nuevos proveedores de modelos de lenguaje y migrar la infraestructura cuando el proyecto lo requiera.

---

## Estado actual del desarrollo

* ✅ Repositorio inicial creado.
* ✅ Documento fundacional (`FOUNDATIONS.md`).
* ✅ Roadmap del proyecto (`ROADMAP.md`).
* 🚧 Diseño del modelo de conocimiento en curso.

---

## Licencia

Pendiente de definir.

---

## Visión

Atanor no pretende ser un chatbot que responda preguntas.

Pretende convertirse en un sistema capaz de comprender, organizar y relacionar conocimiento para ayudar a las personas a aprender de forma más eficiente, manteniendo siempre el vínculo con las fuentes originales y ofreciendo respuestas fundamentadas y verificables.
