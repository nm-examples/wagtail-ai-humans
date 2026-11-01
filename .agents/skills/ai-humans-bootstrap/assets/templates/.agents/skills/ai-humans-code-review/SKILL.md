---
name: ai-humans-code-review
description: Review current Wagtail changes or a requested area of an existing project for actionable defects, requirement gaps, and maintainability problems. Use for a requested code review or an agreed review step; routine implementation checks remain with ai-humans-development.
---

# AI Humans Code Review

Read and follow [ai-humans-development](../ai-humans-development/SKILL.md),
the repository's `AGENTS.md`, and README. The development skill owns shared
scope, verification, Git, and pull-request rules. Load only the local technical
skills relevant to the area under review.

A review is read-only unless fixes are also requested. Inspect the existing
checkout without creating a branch or changing files merely to review them.
Return findings in the chat; publishing comments or a GitHub review requires
the user's instruction. Apply the development workflow before implementing
requested fixes.

## Establish the review target

- Identify the original request, acceptance criteria, and intended users before
  judging the implementation. Use linked issues or supplied requirements when
  available. Distinguish an unmet requirement from an unresolved product choice.
- For **change review**, identify the exact diff. For local uncommitted work,
  include staged, unstaged, and relevant untracked files. For a branch or pull
  request, verify the target branch and compare from the merge base; include
  uncommitted work only when it belongs to the requested review. If no target is
  stated, use the current uncommitted work, or the current branch against the
  verified repository default branch when the working tree is clean. State the
  chosen scope. Ask only when ambiguity would materially change the review.
- For a **broader review**, identify the requested feature, directory, or
  concern and its boundaries. Existing defects within that scope are relevant.
  A general request to review current work does not imply a whole-site audit.
- Follow changed behaviour into callers, queries, models, templates, settings,
  migrations, and tests as needed. A small diff can have consequences outside
  its files. Check the previous behaviour before attributing a regression.

## Apply the review priorities

Use these priorities to direct attention, then order findings by actual impact.
Apply the relevant criteria proportionately; reviewing skills or templates in
the base repository does not require a running application.

| Priority | What to establish |
| --- | --- |
| Requirements and scope | The requested behaviour is complete, relevant edge cases have an intended outcome, and unrelated changes do not obscure review. Identify material design decisions hidden in the implementation. |
| Correctness and regressions | Trace real inputs through the affected flow, including empty, invalid, and error paths. Check compatibility with existing callers, locked dependency versions, and affected development or production configuration. |
| Security, permissions, and publishing | Check authentication and authorization at the actual read or write boundary, validation and escaping, and public versus draft, private, scheduled, or preview content. Follow site and locale boundaries where relevant; being live alone does not establish public visibility. |
| Data integrity and migrations | Check constraints, relation handling, transactions or concurrent writes where relevant, and migration compatibility with existing data and saved revisions. Consider restore, republish, reversibility, and release sequencing when affected. |
| Query performance and caching | Look for repeated queries, unbounded work, and inappropriate media loading in realistic listings. Check invalidation and cache variation by site, locale, permissions, and preview state; justify performance findings with an affected path or measurement. |
| Accessibility and editor experience | Check semantic output, keyboard access, focus, labels, errors, responsive behaviour, and relevant media alternatives. Consider editor validation, choices, preview, saving, and publishing as well as public rendering. |
| Design and maintainability | Prefer existing Wagtail/Django patterns and project conventions. Identify concrete costs from unnecessary abstractions, duplicated rules, misplaced responsibilities, or unjustified dependencies. Tie findings to a failure or maintenance burden rather than personal style. |
| Tests and verification | Check whether coverage demonstrates the requested outcome and would detect the relevant regression, including permission or invalid cases when affected. Identify specific missing scenarios; a low coverage number or absent test alone is not a finding. |
| Documentation and operation | Check affected feature, editor, setup, configuration, and deployment instructions for missing or misleading information. Include migration, dependency/lockfile, and asset workflow changes when relevant. Scale documentation needs to the change. |

## Gather evidence

Verify suspected findings against the actual control flow and the project's
locked framework version. Follow relevant technical skill guidance for API
details. Do not report a hypothetical failure that existing validation,
permissions, or framework behaviour already prevents.

Use the configured Docker, uv, and `just` checks relevant to the review, following
the development skill's verification guidance. Inspect tests and rendered output
where they can resolve a concern. Preserve the working tree; avoid generating
migrations, rewriting snapshots, or changing code to make a review check pass.
Report each check's result or the specific reason it could not run. A passing
suite supports a review but does not establish that every requirement is met.

Separate confirmed findings from assumptions and questions. When a material
concern cannot be established, explain what evidence or decision is missing
without presenting it as a proven defect. Keep existing test failures distinct
from failures introduced by the reviewed changes.

## Report actionable findings

Lead with findings in severity order. For each finding, provide:

- A short title and severity.
- The precise file and smallest useful line range. In a change review, anchor
  to the relevant changed lines where possible and explain any finding elsewhere.
- The concrete trigger, affected user or operation, and resulting impact.
- Supporting code, reproduction, or check evidence and a concise correction
  direction where useful. Keep uncertain assumptions explicit.

Use severity consistently:

- **P0 — critical:** immediate action is needed for an established, widespread
  outage, severe exposure, or destructive behaviour under normal use.
- **P1 — high:** a serious failure or exposure in a supported flow warrants
  fixing before the change is released.
- **P2 — normal:** a material defect, requirement gap, or maintenance problem
  should be corrected in the normal development cycle.
- **P3 — low:** a minor but concrete problem has limited impact.

Judge severity by impact, reach, and likelihood; a security-related label alone
does not determine priority. Do not invent findings to fill a quota, repeat one
root cause as several findings, or report formatting preferences without an
applicable convention and a concrete consequence.

For change reviews, focus findings on introduced problems and missing required
behaviour. Label directly relevant pre-existing problems separately, particularly
when they block verification or safe use; do not attribute them to the change.
For broader reviews, report existing problems within the stated scope.

After findings, include material questions or assumptions, verification results
and gaps, and the reviewed scope. Keep the report proportional to the work.
If there are no findings, say **No actionable findings** and still state the
verification limits. This conclusion does not imply unperformed checks passed.
