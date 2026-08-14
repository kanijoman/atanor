# Development Conventions

# Document Information

| Field        | Value                       |
| ------------ | --------------------------- |
| Project      | Atanor                      |
| Document     | CONVENTIONS                 |
| Status       | 🟢 Active                   |
| Version      | 0.7                         |
| Last Updated | 2026-08-14                  |
| Audience     | Contributors and Developers |

---

# Purpose

This document defines the development conventions followed throughout the Atanor project.

Its objective is to ensure consistency, maintainability and high code quality while enabling contributors to work using shared principles and practices.

Whenever possible, decisions should prioritize simplicity, clarity and long-term maintainability over short-term convenience.

---

# General Principles

Development should always be guided by:

- Keep solutions as simple as possible.
- Prefer readability over cleverness.
- Build only what is currently required.
- Avoid speculative design.
- Validate important domain assumptions before encoding them into software.
- Maintain a clean and understandable Git history.
- Favor consistency over personal preferences.
- Prefer measurable product progress over architectural progress that has no demonstrated user value.

When multiple valid solutions exist, choose the one that minimizes unnecessary complexity while providing the greatest concrete product value.

---

# Product Value over Architectural Prediction

Atanor's architecture must provide a solid and flexible foundation, but **product validation is the primary driver of development**.

Technical decisions must support a concrete user need, improve the user experience, enable a required product capability, or provide a necessary technical foundation for an already validated product direction. Technical work must not become an end in itself.

Architecture should enable product evolution rather than dictate it. The project should prefer solving demonstrated user problems over designing for hypothetical future requirements.

When a new requirement invalidates an existing abstraction, the model should be refactored rather than preserving obsolete structures for the sake of architectural continuity.

A domain model is a tool for expressing the current understanding of the product, not a commitment to a permanent representation of the domain.

From the first user-visible MVP workflow onward, the preferred development loop is:

```text
Concrete user need
        ↓
Product behavior
        ↓
Minimal technical implementation
        ↓
Real user / product validation
        ↓
Learning
        ↓
Refinement or refactoring
        ↓
Next validated need
```

Technical quality remains fundamental. Clean boundaries, maintainable code, appropriate tests and sound engineering practices provide the support required to evolve the product safely. However, when deciding between technical improvements, the preferred option is the one that most directly enables or improves a validated product need, provided the resulting design remains maintainable.

A technical task that cannot be connected to a concrete current product need should normally be deferred unless it addresses a demonstrated reliability, security, correctness or maintainability risk.

---

# Language

To maximize accessibility and encourage external contributions, the project adopts English as its official project language.

The following must be written in English:

- source code;
- identifiers;
- comments;
- documentation;
- commit messages;
- pull requests;
- issues.

Domain content such as laws, regulations, examination material and official documents naturally remains in its original language.

---

# Development Philosophy

Atanor follows an incremental development model.

Infrastructure, frameworks and supporting technologies are introduced only when they solve an existing problem.

This **Just Enough Infrastructure** philosophy prevents unnecessary complexity, keeps the repository lightweight and allows the architecture to evolve naturally.

Domain modeling follows the same principle: do not introduce abstractions merely because they might be useful later.

The preferred development strategy is to prioritize thin, end-to-end product slices that can be validated with real user inputs over building broad infrastructure or a complete domain model in advance.

Every task should leave the project objectively better than before. For product-facing work, “better” should primarily mean that the user can accomplish something useful that they could not accomplish before, or that an existing user workflow becomes materially better.

---

# Product Validation

From the first user-visible MVP workflow onward, product validation is a first-class development concern.

Technical validation asks:

> Does Atanor implement the intended behavior correctly?

Product validation asks:

> Can a user use that behavior and obtain something useful from it?

Both are required, but product validation determines the direction of subsequent development.

Whenever practical, a product-oriented task should identify:

- the user problem being addressed;
- the user-visible capability or experience being improved;
- the evidence that will validate the result;
- the technical implementation required to support that behavior.

A task should not be considered successful solely because its automated tests pass when the intended product behavior has not been meaningfully validated.

Product validation does not require a complete UI. A CLI, API or other minimal interface is sufficient when it allows the actual user-facing behavior to be evaluated meaningfully.

---

# Software Design

The project follows widely accepted software engineering practices.

Whenever applicable:

- Clean Code;
- SOLID principles;
- DRY;
- Separation of Concerns;
- high cohesion;
- low coupling.

Design decisions should favor maintainability over premature optimization.

Domain concepts should be modeled according to validated product needs rather than being derived prematurely from implementation technology or anticipated future features.

---

# Pragmatism

Engineering decisions should be pragmatic.

Theoretical purity should never take precedence over practical value.

When a simpler solution adequately solves the problem, it should be preferred over a more sophisticated alternative.

At the same time, simplicity must not be achieved by hiding important domain distinctions, such as the difference between a requirement, a source and the knowledge supported by that source.

A previously valid abstraction may be changed or removed when real product development demonstrates that it no longer represents the problem adequately.

---

# Test-Driven Development

Test-Driven Development is encouraged whenever it provides clear value.

The preferred workflow is:

1. Understand the requirement.
2. Design the behavior.
3. Write the tests.
4. Implement the solution.
5. Refactor while preserving correctness.

TDD is a development technique rather than a mandatory rule.

## Functional Test Scope

Tests must validate a concrete functional behavior or flow.

A test should have one primary functional responsibility and should fail for a reason that is meaningful to that behavior.

Tests must not be added solely to increase code coverage. Coverage is a consequence of validating relevant functionality, not a target by itself.

When two behaviors can fail independently and represent different functional contracts, they should be covered by separate tests even if they exercise some of the same implementation code.

The physical organization of tests should remain proportional to the project. Independent tests do not necessarily require separate files; a new test file should be introduced when the growing set of related behaviors makes the separation useful.

## Test Isolation and Reproducibility

Tests must be self-contained and reproducible.

A test must:

- create all state it requires;
- not assume pre-existing data or database structures;
- not depend on another test having run before it;
- be executable in an empty testing environment;
- be executable independently as well as as part of the full test suite;
- avoid using development or production data;
- clean up test-specific state when required by the test environment.

Shared fixtures or test infrastructure should only be introduced when they provide a clear benefit without compromising these properties.

The goal is that a clean checkout with the project's declared test dependencies can execute the complete test suite without requiring manually prepared data or infrastructure.

---

# Temporal Data

Timestamps persisted by Atanor represent canonical UTC instants and are independent of the user's timezone.

The persistence layer must store and return timestamps as UTC values. User-local timezone conversion is a presentation concern and belongs to the frontend or another consumer-facing layer.

A timestamp must not be converted to a user's local timezone before persistence.

---

# Git Workflow

Each commit should represent a single logical change.

Commits should:

- be atomic;
- be self-contained;
- compile or pass the applicable checks;
- leave the project in a consistent state.

Commit messages must follow this format:

```text
AT-XXX Change description
```

where `AT-XXX` is the backlog task associated with the change and the description briefly identifies the logical change performed.

A push should normally correspond to a single isolated backlog task, so that introduced changes remain traceable and potential regressions can be associated with a specific task.

---

# Backlog

The backlog defines the implementation plan, not the technical specification.

Implementation details belong in the corresponding commits and technical documentation.

Tasks should remain focused on a single responsibility and should not expand their scope during implementation.

If implementation reveals additional necessary work, that work should be evaluated and, where appropriate, created as a separate task rather than silently expanding the current task.

Tasks should state the concrete product or user value they are intended to deliver whenever the task is product-facing.

---

# Dependencies

New dependencies should be introduced only when they provide clear and immediate value.

Before adding a dependency, contributors should evaluate:

- whether the functionality can reasonably be implemented without it;
- long-term maintenance cost;
- community adoption;
- documentation quality;
- compatibility with the existing architecture.

Avoid introducing libraries solely for convenience.

---

# Documentation

Documentation evolves together with the project.

Documentation should describe validated decisions and sufficiently established domain concepts rather than speculative future designs.

When code changes affect documented behavior or architecture, the corresponding documentation should be updated within the same change whenever practical.

Documentation should remain proportional to the project's needs. Updating a document is not automatically justified by every implementation change; the cost of maintaining the documentation must be weighed against its long-term value.

---

# Continuous Improvement

Conventions are expected to evolve.

When better practices are identified, they should be discussed and incorporated while preserving consistency across the project.

The objective is continuous improvement rather than rigid adherence to historical decisions.
