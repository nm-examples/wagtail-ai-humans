# Project development requirements

For application planning, implementation, fixes, and code review, read and follow
[the repository development skill](.agents/skills/ai-humans-development/SKILL.md).
This is required even when another skill provides technical guidance. The
development skill owns the shared scope, verification, Git, and pull-request rules.

For requested code reviews or an agreed review step, also follow
[the code review skill](.agents/skills/ai-humans-code-review/SKILL.md)
for review priorities, evidence, and findings.

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
For the imported technical skills, preserve their
[provenance and licence material](.agents/skills/PROVENANCE.md) when updating them.

Use the Docker, uv, and `just` workflow documented in [README.md](README.md).
