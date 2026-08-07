# Technology Decisions

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | TECHNOLOGY                  |
| Status       | 🟢 Active                   |
| Version      | 0.2                         |
| Last Updated | 2026-08-07                  |
| Audience     | Contributors and Developers |

---

# Purpose

This document records the technology decisions currently adopted by the Atanor project.

Its purpose is **not** to describe every technology that may eventually be used, but only those that have been formally adopted and currently influence development.

Technology decisions evolve together with the project and should remain aligned with the project's architecture, roadmap and development conventions.

When a technology decision requires additional context or long-term justification, it should be documented through an Architecture Decision Record (ADR).

---

# Technology Selection Principles

Technology choices are guided by the following principles:

* Solve existing problems, not hypothetical ones.
* Prefer mature and well-supported ecosystems.
* Minimize long-term maintenance cost.
* Follow industry standards whenever practical.
* Avoid unnecessary dependencies.
* Introduce infrastructure only when it provides immediate value.

Technology should always support the product, never dictate its architecture.

---

# Adopted Technologies

## Backend

### Python 3.14

**Status:** ✅ Adopted

Python is the primary programming language of the project due to its mature ecosystem for Artificial Intelligence, Natural Language Processing and modern backend development.

The project targets Python 3.14 to benefit from the latest stable language improvements while avoiding unnecessary legacy compatibility.

---

### uv

**Status:** ✅ Adopted

`uv` is used for Python environment and dependency management.

Reasons for adoption:

* Excellent performance.
* Native support for the modern Python packaging ecosystem.
* Full compatibility with `pyproject.toml`.
* Minimal configuration.
* Low maintenance overhead.

---

### pyproject.toml

**Status:** ✅ Adopted

The Python project is configured through `pyproject.toml` following PEP 621.

Project metadata, dependencies and tool configuration are centralized in a single standard file.

---

## Frontend

### Node.js 24 LTS

**Status:** ✅ Adopted

Node.js 24 LTS is the reference runtime for frontend development.

Choosing the current LTS release provides long-term stability while remaining aligned with the modern JavaScript ecosystem.

---

### pnpm

**Status:** ✅ Adopted

`pnpm` is the project's package manager.

Reasons for adoption:

* Fast installation.
* Efficient disk usage.
* Excellent support for monorepositories.
* Wide adoption within the modern frontend ecosystem.

---

# Technologies Deferred

Some technologies are expected to become part of the project but have **not yet been adopted**.

They will only be incorporated when they solve an actual development need.

Examples include:

* FastAPI
* SQLAlchemy
* Pydantic
* React
* Vite
* PostgreSQL
* Docker
* Authentication
* CI/CD
* Observability

Listing them here does **not** imply commitment to their adoption.

---

# Technology Evolution

Technology decisions are expected to evolve.

Whenever a new technology is adopted:

* the decision should be justified;
* this document should be updated;
* any significant architectural impact should be recorded through an ADR.

Technologies that are replaced or discarded should remain traceable through the project's architectural documentation.

---

# Guiding Principle

Atanor follows a **Just Enough Technology** philosophy.

A technology is adopted only when it provides immediate value to the current stage of development.

This approach keeps the project simple, maintainable and adaptable while minimizing unnecessary technical debt.
