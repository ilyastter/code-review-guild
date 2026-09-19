---
name: code-simplifier
description: Use when recently changed code needs a maintainability review or a safe simplification pass that preserves observable behavior, public contracts, and architectural intent across programming languages
---

# Code Simplifier

Review recently changed code for maintainability, then apply only changes that clearly simplify the system. Preserve observable behavior, public APIs, compatibility, and the architectural intent of the change.

This is a language-agnostic workflow. Follow the repository's conventions, language idioms, type system, error-handling model, build tooling, and test commands. Do not assume a JavaScript, Python, or other language-specific solution when the repository provides a different convention.

## Scope

- Start with files changed in the current task, commit, or review. Include nearby callers, implementations, tests, configuration, and documentation when needed to understand a contract.
- Expand beyond the changed area only when the user asks for a broader cleanup or when a local finding cannot be evaluated without its dependencies.
- Read applicable `AGENTS.md`, `CLAUDE.md`, contribution guidance, and project-level configuration before editing.
- Treat existing behavior as the baseline. Identify public entrypoints, serialized data, CLI or protocol behavior, side effects, error behavior, ordering, performance-sensitive paths, and concurrency assumptions that must remain stable.

## Workflow

### 1. Establish the baseline

Inspect the diff and enough surrounding code to explain what changed and why. Locate relevant tests and the repository's normal validation commands. Do not infer that code is dead, duplicated, or safe to move from one file alone; check references and the surrounding design.

### 2. Report high-confidence findings first

Before modifying code, report only findings supported by concrete evidence. For each finding, include:

- severity: `must fix` or `should consider`
- confidence
- file and line or symbol
- evidence in the code or its usage
- why the issue harms maintainability or increases risk
- a small, practical change that would address it

Also record important `acceptable tradeoff` and `not a problem` observations when they prevent likely misinterpretation. If there is no high-confidence simplification, say so and leave the code unchanged.

### 3. Apply only clear simplifications

Make small, local changes that have a strong case for improving clarity or maintainability:

- remove verified dead code, obsolete branches, unused dependencies, or redundant conversions
- simplify control flow, nesting, state transitions, and repeated guards without hiding important behavior
- improve names where the existing name obscures the domain or contract
- consolidate duplicated domain logic only when the behavior and reason to change are genuinely shared
- extract a focused unit when it reduces mental load, and inline a wrapper or abstraction when it adds no meaningful boundary
- make constants explicit when a value is a real domain rule or important invariant, not merely because every literal must be named
- reduce unnecessary coupling, indirection, or invalid states while respecting existing module and architectural boundaries
- strengthen tests around behavior that the refactor could break, without coupling tests to implementation details

Do not optimize for fewer lines. Explicit local code is preferable to clever compact code, speculative generality, or a new layer that exists only to make a pattern fit.

### 4. Verify the result

Run the narrowest relevant tests first, then the project's appropriate broader checks when practical. Use the repository's own test, lint, type-check, build, formatting, and static-analysis commands rather than inventing language-specific commands. Review the final diff for accidental behavior changes, public-contract drift, unrelated edits, and test changes that merely accommodate the implementation.

Report what changed, what was verified, and any checks that could not run. If the repository lacks useful tests, state the remaining confidence and use the strongest available validation instead of pretending the refactor is proven safe.

## Review lenses

Use the main principles as practical lenses, not as a checklist or a reason to force a design pattern:

- **KISS:** look for accidental complexity, opaque control flow, unnecessary layers, and indirection that make local behavior harder to understand.
- **DRY:** look for repeated domain decisions, rules, or transformations. Do not merge code merely because its syntax looks similar when the concepts or change reasons differ.
- **YAGNI:** look for unused extension points, configuration, generic interfaces, adapters, and future-proofing that current requirements do not justify.
- **SoC:** look for mixed responsibilities and boundaries that make behavior, ownership, or testing unclear. Keep cohesive logic together when separation would only add ceremony.
- **SOLID:** improve responsibilities, dependencies, substitutability, and interface size when the current design creates a concrete maintenance problem. Do not introduce classes, interfaces, inheritance, or dependency injection solely to satisfy terminology.

## High-value checks

Consider these areas when evidence points to them:

- dead or unreachable code, commented-out implementations, and obsolete compatibility paths
- excessive or insufficient abstraction, including wrappers, factories, helpers, interfaces, and inheritance
- hardcoded values that should be domain constants or configuration, while preserving intentional fixed rules and local clarity
- duplicated domain logic, feature envy, inappropriate intimacy, and unnecessary coupling
- contracts of functions, classes, records, dataclasses, modules, or services that expose needless parameters, states, optionality, or lifecycle complexity
- brittle, redundant, over-specified, or implementation-coupled tests; also missing characterization coverage for behavior at risk
- comments and documentation that are stale, misleading, or only restate obvious syntax

## Guardrails

- Preserve public names, signatures, schemas, serialization formats, error contracts, CLI/protocol behavior, and side-effect ordering unless the user explicitly requests a breaking change.
- Preserve required performance, security, resource, concurrency, and compatibility properties; a shorter implementation is not automatically equivalent.
- Do not refactor unrelated code, rewrite a subsystem, introduce a dependency, or change architecture without a concrete local benefit and user scope.
- Do not remove a helpful abstraction, split cohesive code, or create a new abstraction merely to satisfy a generic design pattern.
- Do not treat every repeated literal as a magic value or every repeated line as harmful duplication.
- Do not delete tests solely because they are inconvenient, and do not rewrite tests to assert the new implementation rather than the behavior.
- Do not apply a finding when the evidence is weak. Leave a questionable opportunity as a stated recommendation instead of making a speculative change.

This skill complements the focused `review-dry`, `review-kiss`, `review-yagni`, `review-soc`, and `review-solid` skills. Those reviewers remain narrow and read-only; this skill performs only the behavior-preserving simplifications that its evidence supports.
