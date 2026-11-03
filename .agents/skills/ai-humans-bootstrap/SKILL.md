---
name: ai-humans-bootstrap
description: "Bootstrap a new Wagtail CMS site using this repository's uv, Docker, PostgreSQL, and just conventions. Use when creating a new site from an empty project; not for upgrading an existing application, migrating existing data, or deploying to a live host."
---

# AI Humans Bootstrap

Create a working local development stack and a separately buildable production
image. Use PostgreSQL for both environments. This is a repository-local skill;
keep all reusable resources with it and do not require a global installation or
an external reference checkout.

## Inputs and defaults

- Determine the destination, project slug, and display name from the request.
  Ask for the destination if it cannot be inferred; do not reinitialize the
  current application just because the skill lives in its repository.
- Default to Python 3.14, PostgreSQL 18, and settings package `config`. Preserve
  explicit user choices for these defaults. Generated stacks always publish HTTP
  on host port 8000.
- Use the installed uv version for the Docker builder's uv tag. Check current
  official Wagtail/Django compatibility guidance before selecting versions.
  Resolve current compatible Python dependencies and generate a fresh lockfile.

## Bootstrap

1. Inspect the destination and applicable repository instructions. Use an empty
   project directory (an existing Git repository is fine), or bootstrap in place
   when the developer explicitly selects `.` in a fresh `wagtail-ai-humans-base`
   checkout. For an in-place bootstrap, verify the checkout contains only the
   base scaffold and has no local changes to overwrite. Preserve Git history,
   configuration, and unrelated files. Never overwrite an existing application
   or reset databases. Surface actual conflicts before continuing with dependent
   work. Read the bundled
   [development skill](assets/templates/.agents/skills/ai-humans-development/SKILL.md)
   and apply its Git and pull-request workflow to bootstrap work. When the
   destination is its own Git repository, follow its branch workflow before
   generating files.
2. Before generating files, follow the
   [port 8000 preflight](references/configuration.md#port-8000-preflight).
3. Run `uv init --bare --python <version>` and `uv python pin <version>`, then
   `uv add wagtail` in the destination. For a separate destination, run
   `uv run wagtail start config .` there. For an in-place bootstrap, run
   `uv run wagtail start config <empty-temporary-directory>` so the scaffold
   does not collide with the base checkout's dotfiles. Copy the fresh scaffold
   into the checkout, skipping files supplied by the bundled project templates.
   Check for any other collisions before copying.
4. Add `gunicorn`, `psycopg[binary]>=3.2,<4`, and `whitenoise` with uv. Add Ruff
   with `uv add --dev ruff==0.17.3`. Review generated requirements and preserve
   any additional dependencies or necessary constraints in `pyproject.toml`
   before removing `requirements.txt`.
5. Render and copy [the bundled templates](assets/templates/) into the new
   project, including dotfiles, production settings, `AGENTS.md`, and the complete
   bundled `.agents/skills/` tree. This includes `ai-humans-development` and
   `ai-humans-code-review` with their UI metadata, the five Wagtail technical
   skills, and their provenance and licence material. Replace these tokens:

   | Token | Value |
   | --- | --- |
   | `__SITE_SLUG__` | A Compose-compatible slug for the new site |
   | `__SITE_DISPLAY_NAME__` | The human-readable name in its README |
   | `__PYTHON_VERSION__` | Chosen Python minor version |
   | `__RUFF_TARGET_VERSION__` | Ruff's Python target, e.g. `py314` for Python 3.14 |
   | `__POSTGRES_MAJOR__` | Chosen PostgreSQL major version |
   | `__UV_VERSION__` | uv version used to generate the lockfile |

   Do not copy this repository's `pyproject.toml`, lockfile, generated secret
   key, database, uploads, Git history, root `AGENTS.md`, or bootstrap skill folder
   into the new site. Use the bundled project `AGENTS.md`, which has no dependency
   on the source repositories or their mirroring requirements. The seven bundled
   skills are deliberately included; do not copy unrelated installed skills.

   For an in-place bootstrap, replace the base README, `AGENTS.md`, `.gitignore`,
   and the shared skills and provenance with the bundled project versions.
   Remove the inherited bootstrap skill after validation succeeds.
6. Follow [Django settings and validation](references/configuration.md) to merge
   [the Ruff configuration fragment](assets/ruff-pyproject.toml) into the generated
   `pyproject.toml`, adapt the base and development settings, and centralize
   public-site assets in root `assets/`. Inline the generated welcome content
   into the home page template, preserving its appearance. Keep Wagtail and
   third-party package assets in place. Make targeted changes to the fresh
   scaffold instead of copying this site's base settings or assets.
7. Recheck port 8000 before starting the stack. Build and start the development
   stack, apply migrations explicitly, initialize search, and run the validation
   described in that reference. Build the
   production target without needing a live production database or credentials.
   Stop and fix failed checks; do not bypass them to report success. Avoid
   repeating a failing build without a change or new evidence.

Keep the output focused on this setup. Do not add queues, caches, frontend build
systems, hosting-provider configuration, or additional development packages unless
the request calls for them. Ask before installing missing system tools when
that is outside the requested setup; report the precise missing prerequisite.

## Finish

Report the destination, selected versions and port, checks performed, and the
local URL. Supply `just superuser` for interactive admin creation. Report any
validation that could not run, such as Docker checks without an available daemon.

Leave production credentials unset and explain that HTTPS, upload delivery,
email, and backups are completed for the chosen host. Production support here
does not authorize deployment. Treat the validated bootstrap as one coherent
increment for review, including the generated lockfile and project guidance.
Keep existing data and unrelated services intact.
