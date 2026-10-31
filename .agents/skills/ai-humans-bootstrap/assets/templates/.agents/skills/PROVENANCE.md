# Imported Wagtail skills

The following directories are copied unchanged from the `skills/` directory in
the source repository:

- `wagtail-content-modeling/`
- `wagtail-backend/`
- `wagtail-frontend/`
- `wagtail-api/`
- `wagtail-upgrade/`

Upstream project: [wagtail/agent-skills](https://github.com/wagtail/agent-skills).
Import source: [nm-examples/wagtail-agent-skills](https://github.com/nm-examples/wagtail-agent-skills).
Source commit: [`fedcea7a53ee7ba43b9eb825081edd1eee90d14d`](https://github.com/nm-examples/wagtail-agent-skills/tree/fedcea7a53ee7ba43b9eb825081edd1eee90d14d).
This commit includes the API table correction stating that API v3 does not
support `?fields=` projection. There are no application-specific edits inside
the imported directories.

## Licence material

The source repository's root `LICENSE` is preserved verbatim as
[`licenses/wagtail-agent-skills-MIT.txt`](licenses/wagtail-agent-skills-MIT.txt),
including its copyright notice. The source root licence and `plugin.json` declare
MIT, while each imported skill's frontmatter declares BSD-3-Clause. The source
does not supply a separate BSD licence file. This discrepancy remains unresolved;
the original declarations are preserved without selecting or changing a licence.

## Updating the copies

These skills are local to this site and can evolve with its requirements. Use
`ai-humans-development` for changes and user review. Before importing an update,
review an exact source commit and compare it with the existing copies, preserving
intentional local changes. Copy the complete reviewed skill directories and the
supplied licence material, record the source commit and any local differences
here, and validate affected skills and documentation links.

Keep project-specific workflow and tool instructions in this site's `AGENTS.md`
and `ai-humans-development` skill. No sibling checkout or source-maintenance
mirroring is required to use or maintain this site's skills.
