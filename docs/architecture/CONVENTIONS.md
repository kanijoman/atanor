# Conventions

> Convenciones de desarrollo y criterios de calidad aplicables a todo el código de Atanor.

# Información del documento

| Campo                    | Valor                  |
| ------------------------ | ---------------------- |
| Proyecto                 | Atanor                 |
| Documento                | CONVENTIONS            |
| Estado del documento     | 🟢 Activo              |
| Versión del documento    | 0.1                    |
| Última actualización     | 2026-08-07             |

---

# 1. Propósito

Este documento establece las convenciones de desarrollo aplicables al proyecto Atanor.

Su objetivo es garantizar que cualquier contribución mantenga un nivel homogéneo de calidad, facilite el mantenimiento del código y reduzca el coste de incorporación de nuevos colaboradores.

Estas convenciones deberán aplicarse tanto al código desarrollado por personas como al código generado con asistencia de herramientas de Inteligencia Artificial.

---

# 2. Idioma del proyecto

El idioma oficial del proyecto es el inglés.

Esto incluye:

- Código fuente.
- Nombres de módulos, clases, funciones y variables.
- Comentarios.
- Docstrings.
- Documentación técnica.
- Mensajes de error cuando no exista un requisito funcional que indique lo contrario.

El uso de un único idioma facilita la colaboración internacional y evita inconsistencias en el código base.

---

# 3. Principios de desarrollo

Todo el desarrollo del proyecto deberá guiarse por los siguientes principios:

- **Clean Code**.
- **SOLID**.
- **DRY (Don't Repeat Yourself)**.
- **KISS (Keep It Simple, Stupid)**.
- **YAGNI (You Aren't Gonna Need It)**.
- **Pragmatismo sobre dogmatismo**.

Los principios anteriores constituyen una guía para la toma de decisiones, no un conjunto de reglas rígidas.

Cuando dos principios entren en conflicto, se priorizará la solución más simple, mantenible y adecuada para resolver el problema del dominio.

Las excepciones deberán estar justificadas técnicamente y, cuando tengan impacto arquitectónico, documentarse mediante un Architecture Decision Record (ADR).

---

# 4. Organización del código

- Cada módulo deberá tener una única responsabilidad.
- Se favorecerá un bajo acoplamiento entre módulos.
- Las dependencias deberán apuntar hacia el dominio.
- Se evitarán dependencias innecesarias.
- La estructura del código deberá poder evolucionar sin grandes refactorizaciones.

La organización concreta del código evolucionará junto con la arquitectura del proyecto.

---

# 5. Convenciones de implementación

## Tipado

Todo el código nuevo deberá incorporar anotaciones de tipo siempre que resulte razonable.

El tipado forma parte de la documentación del código y contribuye a reducir errores durante el desarrollo.

## Legibilidad

La claridad tendrá prioridad sobre la concisión.

Un código fácil de leer y comprender será preferible a una solución más compacta pero menos expresiva.

## Comentarios

Los comentarios deberán explicar el **por qué**, no el **qué**.

Siempre que sea posible, la intención del código deberá expresarse mediante nombres claros y una estructura sencilla.

## Reutilización

Antes de introducir una nueva abstracción deberá evaluarse si realmente aporta valor al dominio o si añade complejidad innecesaria.

---

# 6. Testing

El desarrollo seguirá preferentemente un enfoque **Test-Driven Development (TDD)** siempre que resulte adecuado para la naturaleza de la tarea.

El flujo recomendado será:

1. Definir el comportamiento esperado.
2. Diseñar las pruebas.
3. Implementar una prueba que falle.
4. Desarrollar la funcionalidad mínima necesaria.
5. Refactorizar manteniendo todas las pruebas en verde.

## Estrategia de pruebas

El objetivo principal no será maximizar el porcentaje de cobertura, sino maximizar la confianza en el comportamiento del sistema.

Se priorizarán:

- Smoke tests.
- Tests funcionales.
- Tests de integración.
- Tests End-to-End.

Las pruebas unitarias deberán centrarse en validar la lógica de negocio y evitar comprobar comportamientos triviales, implementaciones internas o funcionalidades ya garantizadas por librerías de terceros.

---

# 7. Evolución

Estas convenciones evolucionarán junto con el proyecto.

Toda modificación deberá perseguir una mejora objetiva de la mantenibilidad, la calidad del software o la experiencia de desarrollo.

Las convenciones deberán revisarse cuando la evolución del proyecto demuestre que una decisión previa ha dejado de aportar valor.