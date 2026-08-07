# Atanor

# Document Information

| Field        | Value                |
| ------------ | -------------------- |
| Project      | Atanor               |
| Document     | README               |
| Status       | 🟢 Active            |
| Version      | 0.2                  |
| Last Updated | 2026-08-07           |
| Audience     | Users and Developers |

> **An AI-powered knowledge platform for public service exam preparation.**

Atanor is an open-source platform designed to help candidates prepare for competitive public service examinations through structured knowledge management, official source analysis and artificial intelligence.

The first MVP focuses on the Spanish General State Administration examinations, but the architecture is designed to evolve into a general-purpose knowledge management and learning platform.

---

# Goals

The first MVP aims to provide the following capabilities:

* Manage official documentation and study material.
* Organize knowledge into a coherent and reusable domain model.
* Preserve complete traceability between generated content and official sources.
* Assist candidates throughout the learning process.
* Generate explanations, quizzes and study material grounded in verified information.
* Track learning progress over time.

---

# Project Principles

Atanor is developed around a small set of core principles:

* **Knowledge is the core of the platform.**
* **Artificial Intelligence is a tool, not the product itself.**
* **Every generated answer must be traceable to a verifiable source.**
* **Maintainability always takes precedence over unnecessary complexity.**
* **Development is iterative, incremental and domain-driven.**

---

# Development Philosophy

Atanor follows a pragmatic and incremental development process.

The project introduces infrastructure only when it solves an existing problem. Technologies, frameworks and project structure are incorporated as they become necessary, avoiding speculative design and unnecessary complexity.

This philosophy keeps the repository easy to understand, the Git history meaningful and the architecture adaptable as the project evolves.

Development follows modern software engineering practices, including:

* Clean Code
* SOLID principles
* DRY
* Pragmatic design
* Test-Driven Development whenever it provides clear value

---

# Current Status

The project is currently completing the **Foundation Sprint**, during which the development environment, project conventions and architectural principles are being established.

The initial repository structure has been created and the development workflow has been defined before implementing the first application features.

---

# Planned Technology Stack

The initial MVP is expected to be built using:

## Backend

* Python 3.14
* uv
* FastAPI
* SQLAlchemy
* Pydantic

## Frontend

* Node.js 24 LTS
* pnpm
* React
* Vite

## Persistence

* SQLite (MVP)
* PostgreSQL (future iterations)

The technology stack may evolve as the project grows while preserving architectural stability.

---

# Documentation

The main project documentation can be found under the `docs/` directory.

Key documents include:

| Document           | Description                                            |
| ------------------ | ------------------------------------------------------ |
| **FOUNDATIONS.md** | Vision, design principles and architectural decisions. |
| **ROADMAP.md**     | Product roadmap, milestones and long-term planning.    |
| **BACKLOG.md**     | Current development tasks and implementation progress. |
| **CONVENTIONS.md** | Development conventions and coding standards.          |

---

# Current Progress

Completed:

* ✅ Initial repository created.
* ✅ Backend project initialized.
* ✅ Frontend project initialized.
* ✅ Development conventions established.
* ✅ Backlog management rules defined.

In progress:

* 🚧 Sprint 1 · Foundation.

---

# License

License selection is pending.

---

# Vision

Atanor is not intended to become another conversational chatbot.

Its purpose is to become a knowledge platform capable of understanding, organizing and relating information, allowing users to study more effectively while maintaining complete traceability to official sources and providing reliable, verifiable answers.
