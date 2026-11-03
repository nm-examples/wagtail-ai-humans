---
name: ai-humans-development
description: Plan, implement, fix, and review changes to this Wagtail application using focused increments, behaviour-based verification, and clear review evidence. Use for ongoing application development, not bootstrapping a separate site.
---

# AI Humans Development

Use the repository's `AGENTS.md`, README, existing code, and configured tools to
ground decisions. Keep the depth of this workflow proportional to the change:
a small correction needs a brief assessment, not a separate planning document.

Other skills may supplement this workflow; they must not silently replace it,
expand scope, or introduce a different architecture or toolchain. Explain any
conflict and follow the user's instructions and applicable instruction hierarchy.
This guidance does not replace automated checks or developer review.

For a requested code review or an agreed review step, also follow
[ai-humans-code-review](../ai-humans-code-review/SKILL.md) for review priorities,
evidence, and findings. Routine implementation checks remain part of this workflow.

## Assess scope and reviewability

Before editing, identify the intended outcome, affected areas, and significant
design decisions. Inspect the relevant implementation and tests first.

Push back on a plan when it combines independent outcomes, mixes unrelated
refactoring with a feature, hides a foundational decision, or is too vague to
verify. Explain the specific difficulty and suggest smaller, ordered increments.
Reassess if implementation reveals unexpected complexity.

Split by usable behaviour. Keep the models, migrations, templates, and tests
needed to understand one behaviour together. For example, an editable article
page with preview and publication can precede its listing and filters, followed
by API access. Order increments so each builds on earlier work and can be
understood, run, and verified at its own commit boundary. Do not complete the
whole feature first and rely on splitting it into commits afterwards. A small,
coherent change can remain one increment; do not use a rigid line count or a
fixed number of commits as a substitute for judging complexity.

Keep a short record of the agreed increments, completed work, and remaining
scope so review pauses do not lose the rest of the task. Work in the agreed
order and use the review checkpoints in the Git workflow below. Ask for
clarification when an unresolved product or architectural decision materially
changes the outcome; resolve routine implementation choices within the agreed
scope.

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

Before adding a test, identify the meaningful regression it would detect and the
confidence it adds beyond existing coverage. Cover project-owned rules and
important configuration or integration boundaries. For example, saving a
configured snippet through the admin can verify that its registration and fields
work together. Choose the smallest set of tests that provides useful confidence.

Rely on upstream coverage for unmodified framework mechanics. Add focused
coverage when customising those mechanics, integrating them in a significant
way, or reproducing a demonstrated failure. Avoid redundant scenarios and
assertions tied to incidental framework details; a default login redirect or
delete-confirmation flow does not automatically need another project test.

Use test-driven development (TDD) by default for application behaviour that
warrants automated tests: write a behaviour test, observe it fail for the expected
missing behaviour or bug, implement enough to pass, then refactor with tests
passing. An unrelated setup failure does not establish the intended failing case.
For refactoring, establish relevant behaviour coverage before changing code.
State the verification approach before implementation and explain an exception
when another approach fits the task better, such as documentation checks, visual
inspection, generated-migration checks, or an exploratory investigation. Choose
valuable tests before applying TDD; do not add tests merely to follow its sequence.

For existing code with weak coverage, add a focused test of the relevant existing
behaviour when it helps make the change safe. Distinguish intended behaviour from
a suspected existing bug. Prefer observable results over assertions tied to the
implementation's internal calls. Do not add tests that merely mirror code, check
documentation wording, or add no useful confidence for a reversible minor edit.

## Implement within project conventions

Use the project's locked dependency versions when checking framework APIs. Follow
existing Django and Wagtail patterns before adding abstractions or dependencies.
Keep changes focused and preserve unrelated work. Keep unrelated cleanup out of
the change; explain necessary prerequisite work.

Keep project-owned public-site CSS, JavaScript, and design images together in
the root `assets/` directory, under `css/`, `js/`, and `images/`. Use named CSS
classes in separate stylesheets. Add focused files there as needed rather than
creating app-level static folders or forcing everything into one file. Load
shared assets from the base template and page-specific assets through its
`extra_css` and `extra_js` blocks. Leave Wagtail and third-party package assets
in their existing locations.

Use ordinary CSS and JavaScript unless the project explicitly adopts compilation
tooling in a separate change. Django discovers source assets through
`STATICFILES_DIRS`; root `static/` is generated collection output, and `media/`
holds uploads. Do not edit collected files as source assets.

Add useful type annotations to new or substantially changed application functions,
keeping framework overrides compatible. Treat incomplete framework typing as a
specific limitation to investigate, not a reason for broad `Any` or ignore rules.
Python annotations do not type-check Django template variable names.

Prepare queries, filtering, and business decisions in Python. Keep presentation
loops and simple display conditions in templates. Avoid extra abstractions solely
to remove ordinary template syntax. Check rendered output when markup or styling
changes; automated checks alone do not establish visual or accessibility quality.

Use configured tools rather than installing a personal preferred stack. Type
checkers, Tailwind, TypeScript, and CI are not established requirements until
the repository actually adopts them. Treat adopting tooling as an explicit,
reviewable change, and keep `pyproject.toml` and `uv.lock` consistent when changing
Python dependencies.

For Python changes, run `just lint` and `just format-check` where those recipes
are configured. Use `just format` to sort imports and format code, and inspect
automatic fixes before handing over the change. Respect the Ruff configuration,
including the exclusion of migrations from formatting and import sorting.

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

Never weaken tests, checks, or workflow requirements just to make an implementation
pass. Investigate failures rather than deleting assertions, widening suppressions,
or changing configuration to obtain a passing result. Explain necessary changes to
those requirements or expected behaviour. If a check cannot run, state the command,
reason, and resulting gap; do not claim it passed.

Inspect the current increment's complete diff before handing it over. Remove
accidental files, debugging code, and unrelated edits introduced by this work.
Give a reviewer the concrete problem, resulting behaviour, significant decisions,
checks and results, and any remaining limitations. Include practical steps to
try the feature when useful.
Keep the handoff understandable without the chat history, and distinguish
completed work from proposed follow-up increments.

## Git workflow

Apply these requirements unless the user gives different Git instructions. They
guide Git decisions; they do not imply hooks, CI enforcement, or numerical
commit-size limits are configured.

1. **Start new work on an approved branch.** Before implementation, propose a
   descriptive branch name reflecting the requested changes and wait for developer
   approval before creating it. Normally base the branch on the repository's default
   branch; identify that branch rather than assuming its name. If the work depends
   on unmerged changes or needs another base, explain why and propose the base
   alongside the branch name. No fixed prefix is required; category prefixes such
   as `feat/`, `bugfix/`, and `docs/` are suitable. Preserve existing uncommitted
   work and keep unrelated changes out of the new branch's commits.
2. **Plan an ordered series of reviewable commits.** Describe the intended
   commits briefly before substantial work, including dependencies and the usable
   outcome of each. Keep each behaviour's relevant implementation, tests,
   migrations, and documentation together. Make the sequence easy for a developer
   to review and check out one step at a time; avoid one whole-feature commit when
   the work has distinct, usable increments. Keep inseparable changes together.
   A small correction can be a single commit without a separate written plan.
3. **Stop for developer review at each increment.** Complete the current
   increment and its relevant checks, then leave its changes unstaged and
   uncommitted. Give a concise handoff in the chat that states what is done so
   far, what this increment makes usable, the files or entry points to review,
   checks and results, limitations, practical steps to try it, and what remains.
   Name the proposed commit and the next increment, if any, so the developer
   knows exactly what can be reviewed now and what continuing would involve.

   Ask the developer to review the increment and authorise committing it and,
   if work remains, continuing. End the turn and wait before committing or
   starting later implementation increments. Commit approval covers the reviewed increment;
   it does not by itself authorise continuing. The developer can authorise both
   actions together, for example with "commit and continue"; do not request that
   same approval again. A request to implement the overall feature does not
   waive these checkpoints or authorise commits. If the developer explicitly
   requests uninterrupted implementation or batch review, follow that preference
   while preserving coherent commit boundaries and the authorisation required
   for commits and remote actions.

   Automated checks and the agent's own diff inspection do not replace developer
   review. Verification remains proportional to the change. Do not commit
   unfinished work or unresolved relevant failures; explain any verification gap
   and leave the increment uncommitted when it cannot be established as ready.
4. **Review the staged diff before every commit.** After the user authorises a
   commit, inspect Git status and distinguish existing user changes from this
   task's changes. Stage only the intended files or hunks, inspect the complete
   staged diff, and run
   `git diff --cached --check`. Check for accidental files, unrelated edits, secrets,
   and the reported verification results. Do not include someone else's staged
   changes; ask when overlapping changes cannot be separated safely. Use a short,
   imperative commit subject with an appropriate prefix: `feat:`, `fix:`, `docs:`,
   `refactor:`, `test:`, or `chore:`. Describe the actual changes included. Add a body
   only when useful to explain the reason or a significant decision.
5. **Reassess oversized changes.** Use changed-file and line counts as signals to
   inspect scope, not hard thresholds. Split independent behaviours and unrelated
   refactoring. Keep inseparable changes together and explain an unusually broad
   commit when its coherence is not obvious. Do not split simply to meet a count.
6. **Report commits and remaining work.** Verify Git status after committing and
   report each repository's commit IDs, the increment's completed outcome, and
   remaining work or uncommitted changes. State the next increment and whether
   continuing is authorised or awaiting the developer's decision. Distinguish
   pre-existing user changes from unfinished work.

Keep commits local unless the user explicitly approves a push as described below.
Merging requires an explicit user request. Do not rewrite existing commits or
change repository configuration to satisfy this workflow. If the destination is
not its own Git repository, report that no commit was made rather than committing
into an enclosing repository. For mirrored skill changes, verify the copies match
and obtain explicit user authorisation before committing the corresponding reviewed
increment in each repository; report any partial completion if one repository
cannot be updated or committed.

## Remote actions and pull requests

Obtain explicit user approval before each push to a remote and before creating
any pull request, including a draft. Approval to implement or commit changes does
not authorise either action; approval to push does not authorise creating a pull
request. Prepare the concrete action details before asking: the remote, target
branch, and included commits for a push; the source and base branches, title, and
description for a pull request.

Create every pull request as a draft. Leave it as a draft until the user explicitly
approves marking it ready for review.

Every pull request needs a description. Use the minimum content needed to explain
what changed and why. Include testing notes where useful, particularly verification
gaps or steps a reviewer should try. Add screenshots when they help explain visual
changes. Describe the changes actually included in the pull request, without
unrelated context or unnecessary boilerplate.
