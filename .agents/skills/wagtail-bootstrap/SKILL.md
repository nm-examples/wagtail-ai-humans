---
name: wagtail-bootstrap
description: "Bootstrap a new Wagtail CMS site using this repository's uv, Docker, PostgreSQL, and just conventions. Use when creating a new site from an empty project; not for upgrading an existing application, migrating existing data, or deploying to a live host."
---

# Wagtail Bootstrap

Create a working local development stack and a separately buildable production
image. Use PostgreSQL for both environments. This is a repository-local skill;
keep all reusable resources with it and do not require a global installation or
an external reference checkout.

## Inputs and defaults

- Determine the destination, project slug, and display name from the request.
  Ask for the destination if it cannot be inferred; do not reinitialize the
  current application just because the skill lives in its repository.
- Default to Python 3.14, PostgreSQL 18, settings package `config`, and host
  HTTP port 8000. Preserve explicit user choices. If 8000 is occupied, choose
  and report an available loopback port for the new stack.
- Use the installed uv version for the Docker builder's uv tag. Check current
  official Wagtail/Django compatibility guidance before selecting versions.
  Resolve current compatible Python dependencies and generate a fresh lockfile.

## Bootstrap

1. Inspect the destination and applicable repository instructions. Proceed in
   an empty project directory, allowing an existing Git repository. Do not
   overwrite existing application files or reset databases. Surface actual
   conflicts before continuing with dependent work. If the destination is its own
   Git repository, follow the bundled development skill's branch workflow before
   generating files: propose a descriptive branch name and base, normally the
   default branch, and wait for developer approval before creating the branch.
   No fixed branch-name prefix is required.
2. Run `uv init --bare --python <version>` and `uv python pin <version>`, then
   `uv add wagtail` and `uv run wagtail start config .` in the destination.
3. Add `gunicorn`, `psycopg[binary]>=3.2,<4`, and `whitenoise` with uv. Review
   generated requirements and preserve any additional dependencies or necessary
   constraints in `pyproject.toml` before removing `requirements.txt`.
4. Render and copy [the bundled templates](assets/templates/) into the new
   project, including dotfiles, production settings, `AGENTS.md`, and the bundled
   `.agents/skills/wagtail-development/` directory with its UI metadata. Replace
   these tokens:

   | Token | Value |
   | --- | --- |
   | `__SITE_SLUG__` | A Compose-compatible slug for the new site |
   | `__SITE_DISPLAY_NAME__` | The human-readable name in its README |
   | `__PYTHON_VERSION__` | Chosen Python minor version |
   | `__POSTGRES_MAJOR__` | Chosen PostgreSQL major version |
   | `__UV_VERSION__` | uv version used to generate the lockfile |
   | `__HTTP_PORT__` | Available host HTTP port; container port stays 8000 |

   Do not copy this repository's `pyproject.toml`, lockfile, generated secret
   key, database, uploads, Git history, root `AGENTS.md`, or bootstrap skill folder
   into the new site. Use the bundled project `AGENTS.md`, which has no dependency
   on the source repositories or their mirroring requirements. The development
   skill is deliberately included; do not copy unrelated installed skills.
5. Follow [Django settings and validation](references/configuration.md) to adapt
   the newly generated base and development settings and centralize public-site
   assets in root `assets/`. Preserve the generated welcome page's appearance and
   keep Wagtail and third-party package assets in place. Make targeted changes to
   the fresh scaffold instead of copying this site's base settings or assets.
6. Build and start the development stack, apply migrations explicitly, initialize
   search, and run the validation described in that reference. Build the
   production target without needing a live production database or credentials.
   Stop and fix failed checks; do not bypass them to report success. Avoid
   repeating a failing build without a change or new evidence.

Keep the output focused on this setup. Do not add queues, caches, frontend build
systems, hosting-provider configuration, or optional development packages unless
the request calls for them. Ask before installing missing system tools when
that is outside the requested setup; report the precise missing prerequisite.

## Finish

Report the destination, selected versions and port, checks performed, and the
local URL. Supply `just superuser` for interactive admin creation. Report any
validation that could not run, such as Docker checks without an available daemon.

Leave production credentials unset and explain that HTTPS, upload delivery,
email, and backups are completed for the chosen host. Production support here
does not authorize deployment. Follow the bundled
[development skill's Git workflow](assets/templates/.agents/skills/wagtail-development/SKILL.md#git-workflow):
treat the validated bootstrap as one coherent increment and leave it unstaged and
uncommitted for user review, including the generated lockfile and project guidance.
Commit only after the user explicitly authorises committing the reviewed changes
and when the destination is its own Git repository. Review the staged diff before
that commit.
If the destination is not its own Git repository, report that no commit was made;
do not commit into an enclosing source repository. Report the commit ID and any
remaining work. Use a concise, imperative commit subject with an appropriate type
prefix, following the development skill. Each push and pull-request creation
requires explicit approval; prepare the concrete action details and any
pull-request text before asking. Create every pull request as a draft, with a
concise description of what changed and why, plus testing notes and screenshots
where useful. Obtain approval before marking it ready for review. Merging requires
an explicit request. Keep existing data and unrelated services intact.
