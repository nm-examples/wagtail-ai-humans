---
name: wagtail-development
description: Plan, implement, fix, and review changes to this Wagtail application using focused increments, behaviour-based verification, and clear review evidence. Use for ongoing application development, not bootstrapping a separate site.
---

# Wagtail development

Use the repository's `AGENTS.md`, README, existing code, and configured tools to
ground decisions. Keep the depth of this workflow proportional to the change:
a small correction needs a brief assessment, not a separate planning document.

## Assess scope and reviewability

Before editing, identify the intended outcome, affected areas, and significant
design decisions. Inspect the relevant implementation and tests first.

Push back on a plan when it combines independent outcomes, mixes unrelated
refactoring with a feature, hides a foundational decision, or is too vague to
verify. Explain the specific difficulty and suggest smaller, ordered increments.
Reassess if implementation reveals unexpected complexity.

Split by usable behaviour. Keep the models, migrations, templates, and tests
needed to understand one behaviour together. For example, an editable article
page can precede its listing, categories, and related articles. Do not use a
rigid line count as a substitute for judging complexity.

Splitting work does not cancel the remaining requested scope. Complete authorised
increments in order when the direction is clear. Ask for clarification when an
unresolved product or architectural decision materially changes the outcome;
routine implementation choices do not require another approval.

## Establish meaningful verification

Describe concrete expected outcomes before implementation, using the user's
requirements as the source rather than deriving expectations from generated code.
Include relevant empty, invalid, and permission cases, without inventing a large
test matrix for every change. Resolve material ambiguity instead of encoding an
assumption as a requirement.

Select checks that can detect the relevant failure. For rendered content, assert
expected text, destinations, or visibility; a successful HTTP response alone does
not establish that the right content appeared. For editor-facing features,
consider validation, preview, and publishing where affected.

For existing code with weak coverage, add a focused test of the relevant existing
behaviour when it helps make the change safe. Distinguish intended behaviour from
a suspected existing bug. Prefer observable results over assertions tied to the
implementation's internal calls. Do not add tests that merely mirror code, check
documentation wording, or add no useful confidence for a reversible minor edit.

## Implement within project conventions

Use the project's locked dependency versions when checking framework APIs. Follow
existing Django and Wagtail patterns before adding abstractions or dependencies.
Keep unrelated cleanup out of the change; explain necessary prerequisite work.

Add useful type annotations to new or substantially changed application functions,
keeping framework overrides compatible. Treat incomplete framework typing as a
specific limitation to investigate, not a reason for broad `Any` or ignore rules.
Python annotations do not type-check Django template variable names.

Prepare queries, filtering, and business decisions in Python. Keep presentation
loops and simple display conditions in templates. Avoid extra abstractions solely
to remove ordinary template syntax. Check rendered output when markup or styling
changes; automated checks alone do not establish visual or accessibility quality.

Use configured tools rather than installing a personal preferred stack. Type
checkers, Ruff, Tailwind, TypeScript, and CI are not established requirements until
the repository actually adopts them. Treat adopting tooling as an explicit,
reviewable change, and keep `pyproject.toml` and `uv.lock` consistent when changing
Python dependencies.

## Verify and prepare the change for review

Use the development commands in the README and `justfile`. For application
changes, run `just check` and the relevant `just test` labels; use the full suite
when the change affects shared behaviour. For model changes, include the required
migrations and run `just manage makemigrations --check --dry-run`. The
`just manage-once` recipe can run Django commands when the web container is not
running; it may start the development database.

Run any additional relevant checks already configured in the repository. For
instruction-only or documentation changes, check references, consistency, and
formatting; validate changed skills with the skill validator when available.
Do not run the application suite solely for a prose change.

Investigate failures rather than deleting assertions, widening suppressions, or
changing configuration to obtain a passing result. Changes to expected behaviour
or checks need their own explanation. If a check cannot run, state the command,
reason, and resulting gap; do not claim it passed.

Inspect the complete diff before finishing. Remove accidental files, debugging
code, and unrelated edits introduced by this work. Give a reviewer the concrete
problem, resulting behaviour, significant decisions, checks and results, and any
remaining limitations. Include practical steps to try the feature when useful.
Keep the handoff understandable without the chat history, and distinguish
completed work from proposed follow-up increments.
