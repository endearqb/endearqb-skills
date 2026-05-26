---
name: readme-first-builder
description: Initialize or upgrade a project to the full README First architecture from endearqb/ReadmeFirst. Use only when the user asks to initialize README First, install the README First framework, create the complete AGENTS.md + README.md + .ai/changes + .ai/decisions structure, or retrofit a repository with the README First architecture. After initialization, normal project work should follow the target project's AGENTS.md instead of this skill.
---

# README First Builder

## Purpose

Use this skill as a one-time initializer or upgrader for a project-level README First architecture. Do not use it as the default way to write every README after a project already has `AGENTS.md`; once initialized, the target project's own `AGENTS.md` becomes the operating protocol.

## Canonical Source

Read `references/readmefirst-source.md` for the upstream repository and file roles. The canonical project is `endearqb/ReadmeFirst`:

- `README.md`: principle and architecture explanation.
- `AGENTS.md`: executable agent protocol.

When network access is available, inspect the latest upstream files before initializing. If network is unavailable, explain that the initialization is based on the locally known structure and recommend a later sync.

## Initialization Workflow

1. Inspect the target project root and confirm whether `AGENTS.md`, `README.md`, and `.ai/` already exist.
2. If `AGENTS.md` is missing, create it from the upstream ReadmeFirst `AGENTS.md` content, then adapt only project-specific placeholders if necessary.
3. If `AGENTS.md` already exists, merge the README First protocol into it without overwriting local rules. Keep stricter or project-specific local rules.
4. Ensure the root `README.md` acts as the project map: purpose, setup, commands, top-level directory responsibilities, and links to important directory READMEs.
5. Create `.ai/changes/` and `.ai/decisions/` if missing. Add lightweight starter templates only when useful.
6. Add or update directory-level `README.md` files only for key long-lived directories. Do not cover generated, dependency, cache, build, log, or temporary directories.
7. Record the initialization in `.ai/changes/YYYY-MM-DD.md`.
8. Verify paths and commands mentioned in the generated docs.

## Existing File Rules

- Never overwrite an existing `AGENTS.md` or `README.md` blindly.
- Treat existing project rules as local authority unless they conflict with safety or the user's explicit request.
- Preserve user-authored prose and append or merge README First sections.
- If the upstream `AGENTS.md` conflicts with existing project instructions, report the conflict and choose the least destructive merge.

## Handoff After Initialization

End by telling future agents to follow the newly created or merged project `AGENTS.md`. For later ordinary code, documentation, review, or refactor tasks, use the project's own `AGENTS.md` and relevant directory READMEs rather than re-triggering this skill.
