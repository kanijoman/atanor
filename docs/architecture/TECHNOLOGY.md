# Technology

> Decisiones tecnológicas adoptadas para el desarrollo de Atanor.

# Información del documento

| Campo                    | Valor                  |
| ------------------------ | ---------------------- |
| Proyecto                 | Atanor                 |
| Documento                | TECHNOLOGY             |
| Estado del documento     | 🟢 Activo              |
| Versión del documento    | 0.1                    |
| Última actualización     | 2026-08-07             |

---

# 1. Propósito

Este documento recoge las decisiones tecnológicas adoptadas para el desarrollo de Atanor.

Su objetivo no es listar todas las tecnologías que podrían utilizarse en el futuro, sino documentar únicamente aquellas decisiones que condicionan el desarrollo actual del proyecto.

Las decisiones tecnológicas se revisarán de forma iterativa conforme evolucionen los requisitos del producto y quedarán reflejadas tanto en este documento como, cuando sea necesario, en los correspondientes Architecture Decision Records (ADR).

---

# 2. Tecnologías adoptadas

## Lenguaje de programación

### Python 3.13

**Estado:** ✅ Adoptado

**Justificación**

Python ofrece el ecosistema más maduro para el desarrollo de aplicaciones basadas en Inteligencia Artificial y Procesamiento del Lenguaje Natural, principales pilares tecnológicos de Atanor.

La elección de la versión 3.13 responde al objetivo de construir el proyecto sobre una versión estable y moderna del lenguaje, aprovechando las mejoras de rendimiento, tipado y mantenimiento del ecosistema Python.

---

## Gestión del proyecto

### pyproject.toml

**Estado:** ✅ Adoptado

**Justificación**

Toda la configuración del proyecto se centralizará en el archivo `pyproject.toml`, siguiendo el estándar actual del ecosistema Python.

Esto permite mantener una única fuente de configuración para herramientas, dependencias y metadatos del proyecto.

---

## Gestión de dependencias

### uv

**Estado:** ✅ Adoptado

**Justificación**

Se utilizará **uv** como gestor de entornos virtuales y dependencias.

Su elección responde a los siguientes criterios:

- Alto rendimiento.
- Compatibilidad con el estándar `pyproject.toml`.
- Simplicidad de uso.
- Bajo coste de mantenimiento.
- Amplia compatibilidad con el ecosistema Python.

---

# 3. Decisiones pendientes

En el momento de redactar este documento todavía no se han tomado decisiones sobre:

- Framework de aplicación.
- Persistencia de datos.
- Sistema de migraciones.
- Framework de validación.
- Framework para APIs.
- Integración con modelos de lenguaje.
- Estrategia RAG.
- Sistema de autenticación.
- Contenedorización.
- Integración continua.
- Observabilidad.
- Despliegue.

Estas decisiones se incorporarán cuando resulten necesarias para implementar nuevas funcionalidades del producto.

---

# 4. Evolución

Este documento evolucionará junto con el proyecto.

Solo se añadirán nuevas tecnologías cuando exista una decisión firme sobre su adopción. Las tecnologías descartadas o sustituidas deberán quedar reflejadas mediante un Architecture Decision Record (ADR) para preservar el contexto histórico de las decisiones.