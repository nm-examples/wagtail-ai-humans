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

Choose and review an exact source commit. Compare its complete skill directories
with these copies, then copy the reviewed updates and preserve the supplied
licence material. Record the new commit here and describe any intentional local
differences. Validate the affected skills, check documentation links, and inspect
the complete diff before user review under `ai-humans-development`.

Keep project-specific workflow and tool instructions in the project's
`AGENTS.md` and `ai-humans-development` skill so the imported content stays easy
to compare with its source. The imported skills supplement that workflow.

These copies belong to this application only. They are not mirrored into
`wagtail-ai-humans-base` or bundled in the bootstrap templates. Adding them to
generated sites would be a separate change. The application does not require
the sibling source checkout to use these skills.
