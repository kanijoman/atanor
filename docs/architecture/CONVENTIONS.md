# Development Conventions

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | CONVENTIONS                 |
| Status       | 🟢 Active                   |
| Version      | 0.2                         |
| Last Updated | 2026-08-07                  |
| Audience     | Contributors and Developers |

---

# Purpose

This document defines the development conventions followed throughout the Atanor project.

Its objective is to ensure consistency, maintainability and high code quality while enabling contributors to work using shared principles and practices.

Whenever possible, decisions should prioritize simplicity, clarity and long-term maintainability over short-term convenience.

---

# General Principles

Development should always be guided by the following principles:

* Keep solutions as simple as possible.
* Prefer readability over cleverness.
* Build only what is currently required.
* Avoid speculative design.
* Maintain a clean and understandable Git history.
* Favor consistency over personal preferences.

Whenever multiple valid solutions exist, choose the one that minimizes unnecessary complexity.

---

# Language

To maximize accessibility and encourage external contributions, the project adopts English as its official language.

The following must be written in English:

* Source code.
* Identifiers.
* Comments.
* Documentation.
* Commit messages.
* Pull requests.
* Issues.

Domain content (laws, regulations, examination material and official documents) naturally remains in its original language.

---

# Development Philosophy

Atanor follows an incremental development model.

Infrastructure, frameworks and supporting technologies are introduced only when they solve an existing problem.

This **Just Enough Infrastructure** philosophy prevents unnecessary complexity, keeps the repository lightweight and allows the architecture to evolve naturally.

Every task should leave the project objectively better than before.

---

# Software Design

The project follows widely accepted software engineering practices.

Whenever applicable:

* Clean Code
* SOLID principles
* DRY
* Separation of Concerns
* High cohesion
* Low coupling

Design decisions should always favor maintainability over premature optimization.

---

# Pragmatism

Engineering decisions should be pragmatic.

Theoretical purity should never take precedence over practical value.

When a simpler solution adequately solves the problem, it should be preferred over a more sophisticated alternative.

---

# Test-Driven Development

Test-Driven Development is encouraged whenever it provides clear value.

The preferred workflow is:

1. Understand the requirement.
2. Design the behavior.
3. Write the tests.
4. Implement the solution.
5. Refactor while preserving correctness.

TDD is considered a development technique rather than a mandatory rule.

---

# Git Workflow

Each commit should represent a single logical change.

Commits should:

* Be atomic.
* Be self-contained.
* Compile successfully.
* Leave the project in a consistent state.

Large changes should be split into multiple commits whenever practical.

---

# Backlog

The backlog defines the implementation plan, not the technical specification.

Implementation details belong in the corresponding commits.

Tasks should remain focused on a single responsibility and should not expand their scope during implementation.

---

# Dependencies

New dependencies should be introduced only when they provide clear and immediate value.

Before adding a dependency, contributors should evaluate:

* Whether the functionality can reasonably be implemented without it.
* Long-term maintenance cost.
* Community adoption.
* Documentation quality.
* Compatibility with the existing architecture.

Avoid introducing libraries solely for convenience.

---

# Documentation

Documentation evolves together with the project.

Documentation should describe implemented decisions rather than speculative future designs.

Whenever code changes affect documented behavior or architecture, the corresponding documentation should be updated within the same change whenever possible.

---

# Continuous Improvement

Conventions are expected to evolve.

When better practices are identified, they should be discussed and incorporated while preserving consistency across the project.

The objective is continuous improvement rather than rigid adherence to historical decisions.
