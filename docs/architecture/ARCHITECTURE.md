# Architecture

> Decisiones arquitectónicas y principios de diseño que guían la evolución técnica de Atanor.

# Información del documento

| Campo                 | Valor                  |
| --------------------- | ---------------------- |
| Proyecto              | Atanor                 |
| Documento             | ARCHITECTURE           |
| Estado del documento  | 🟢 Activo              |
| Versión del documento | 0.1                    |
| Última actualización  | 2026-08-07             |
| Estado de la arquitectura | 🟡 En evolución    |

---

# 1. Propósito

Este documento define la arquitectura de Atanor y las decisiones de diseño que condicionan su evolución.

No pretende describir una arquitectura definitiva ni anticipar componentes futuros. Su objetivo es documentar únicamente aquellas decisiones que resultan necesarias para el estado actual del proyecto.

La arquitectura evolucionará de forma iterativa, acompañando al dominio y a las necesidades reales del producto.

---

# 2. Principios arquitectónicos

## El dominio dirige la arquitectura

Las decisiones técnicas estarán subordinadas al modelo del dominio. Ningún framework, librería o tecnología condicionará el diseño del sistema.

## Evolución incremental

Solo se introducirán nuevos componentes cuando exista una necesidad funcional que los justifique.

## Simplicidad

Se priorizará la solución más sencilla que satisfaga los requisitos actuales, evitando sobreingeniería y dependencias innecesarias.

## Bajo acoplamiento

Los distintos módulos del sistema deberán comunicarse mediante interfaces bien definidas, minimizando las dependencias entre ellos.

## Alta cohesión

Cada módulo tendrá una única responsabilidad claramente definida.

## Decisiones reversibles

Siempre que sea posible, las decisiones técnicas deberán ser fáciles de sustituir en el futuro.

---

# 3. Arquitectura actual

En la versión actual del proyecto únicamente se han establecido las siguientes decisiones estructurales.

## Organización del repositorio

```text
atanor/

├── docs/
│   ├── architecture/
│   ├── foundation/
│   ├── roadmap/
│   └── adr/
│
├── src/
├── tests/
└── scripts/
```

Esta estructura podrá evolucionar cuando el crecimiento del proyecto lo justifique.

## Organización del código

Todavía no se ha definido una arquitectura interna para el código fuente.

La organización de `src/` se decidirá cuando aparezcan los primeros componentes funcionales del sistema.

---

# 4. Decisiones pospuestas

En este momento todavía no se han tomado decisiones sobre los siguientes aspectos:

- Lenguaje y versión objetivo.
- Framework de aplicación.
- Persistencia.
- Modelo de datos.
- Infraestructura.
- Sistema de autenticación.
- Integración con modelos de lenguaje.
- Estrategia RAG.
- Observabilidad.
- Despliegue.

Estas decisiones se incorporarán únicamente cuando sean necesarias para implementar funcionalidades del producto.

---

# 5. Evolución de la arquitectura

Las decisiones arquitectónicas relevantes se documentarán mediante ADR (Architecture Decision Records).

Cada ADR deberá responder, como mínimo, a las siguientes preguntas:

- ¿Qué decisión se ha tomado?
- ¿Qué problema resuelve?
- ¿Qué alternativas se consideraron?
- ¿Por qué se eligió esta solución?

Los ADR complementan este documento y permiten comprender la evolución arquitectónica del proyecto sin modificar continuamente sus principios fundamentales.