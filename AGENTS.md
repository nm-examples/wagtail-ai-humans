# Project development requirements

For application planning, implementation, fixes, and code review, read and follow
[the repository development skill](.agents/skills/wagtail-development/SKILL.md).
This is required even when another skill provides technical guidance. The
development skill owns the shared scope, verification, Git, and pull-request rules.

Use the relevant local technical skills alongside that workflow:

- [Content modeling](.agents/skills/wagtail-content-modeling/SKILL.md): page types,
  snippets, fields, StreamField, editor interfaces, and content migrations.
- [Backend](.agents/skills/wagtail-backend/SKILL.md): queries, search, permissions,
  publishing, workflows, and runtime behavior.
- [Frontend](.agents/skills/wagtail-frontend/SKILL.md): templates, accessibility,
  media rendering, metadata, and editor previews.
- [API](.agents/skills/wagtail-api/SKILL.md): API v3 configuration and integrations.
- [Upgrade](.agents/skills/wagtail-upgrade/SKILL.md): Wagtail upgrade planning and
  implementation.

Read only the technical skills relevant to the task. Follow the project's
configured tools and commands when applying their verification guidance.

Use the Docker, uv, and `just` workflow documented in [README.md](README.md).
For creating a separate new site, use the
[bootstrap skill](.agents/skills/wagtail-bootstrap/SKILL.md).
When changing `wagtail-development` or `wagtail-bootstrap`, follow the
[copy and mirroring instructions](README.md#project-folders).
For the five imported technical skills, follow their
[provenance and update notes](.agents/skills/PROVENANCE.md).
