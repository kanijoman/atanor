# Technology Decisions

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | TECHNOLOGY                  |
| Status       | 🟢 Active                   |
| Version      | 0.3                         |
| Last Updated | 2026-08-10                  |
| Audience     | Contributors and Developers |

---

# Purpose

This document records technology decisions currently adopted by Atanor.

It does not describe technologies that might be useful in the future unless they have been formally adopted.

Technology decisions must remain aligned with the product's architecture, roadmap and development conventions.

When a technology decision requires significant architectural justification, it should be documented through an Architecture Decision Record (ADR).

---

# Technology Selection Principles

Technology choices are guided by:

- Solve existing problems, not hypothetical ones.
- Prefer mature and well-supported ecosystems.
- Minimize long-term maintenance cost.
- Follow standards whenever practical.
- Avoid unnecessary dependencies.
- Introduce infrastructure only when it provides immediate value.
- Keep the technology layer subordinate to the domain model.

Technology should support the product rather than dictate its architecture.

---

# Adopted Technologies

## Backend

### Python 3.14

**Status:** ✅ Adopted

Python is the primary backend language.

The project targets Python 3.14 as the currently selected runtime.

The language choice is also compatible with Atanor's expected future work in information processing, natural language processing and AI-assisted capabilities, but those future capabilities do not by themselves justify additional dependencies.

---

### uv

**Status:** ✅ Adopted

`uv` is used for Python environment and dependency management.

Reasons include:

- fast environment and dependency operations;
- support for the modern Python packaging ecosystem;
- compatibility with `pyproject.toml`;
- minimal configuration.

---

### pyproject.toml

**Status:** ✅ Adopted

The Python project is configured through `pyproject.toml` following modern Python packaging conventions.

Project metadata, dependencies and tool configuration are centralized there.

---

## Frontend

### Node.js 24 LTS

**Status:** ✅ Adopted

Node.js 24 LTS is the reference runtime for frontend development.

---

### pnpm

**Status:** ✅ Adopted

`pnpm` is the frontend package manager.

Reasons include:

- efficient installation;
- efficient disk usage;
- strong support for modern JavaScript projects;
- good support for workspace-based repositories.

---

# Technologies Deferred

The following technologies remain deferred unless an actual requirement justifies their adoption:

- FastAPI
- SQLAlchemy
- Pydantic
- React
- Vite
- PostgreSQL
- Docker
- Authentication
- CI/CD
- Observability

Their presence in this list is not a commitment to adopt them.

In particular, the current domain-model work must not be used as justification for selecting a persistence technology before the conceptual model has been sufficiently validated.

---

# Technology and Domain Model

Technology selection must follow domain understanding.

At the current stage, the product domain is being refined around:

- requirements;
- knowledge scopes;
- knowledge blueprints;
- knowledge entities and assertions;
- provenance and evidence;
- learning paths.

The persistence strategy should be selected only after the conceptual model and its required relationships are sufficiently understood.

---

# Technology Evolution

Whenever a new technology is adopted:

- the decision should be justified;
- this document should be updated;
- significant architectural impact should be recorded through an ADR.

Technologies that are replaced or discarded should remain traceable through the project's architectural documentation.

---

# Guiding Principle

Atanor follows a **Just Enough Technology** philosophy.

A technology is adopted only when it provides clear value to the current stage of development.

The simplest technology that adequately supports the validated domain should be preferred.
