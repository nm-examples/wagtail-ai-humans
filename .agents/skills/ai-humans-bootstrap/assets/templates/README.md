# __SITE_DISPLAY_NAME__

Wagtail CMS with Python __PYTHON_VERSION__, PostgreSQL __POSTGRES_MAJOR__, uv,
Docker Compose, and just. Dependencies are resolved for this site and recorded
in `pyproject.toml` and `uv.lock`.

## Development workflow

[AGENTS.md](AGENTS.md) directs application work to the repository-local
[`ai-humans-development` skill](.agents/skills/ai-humans-development/SKILL.md).
The skill owns the shared development, Git, and pull-request rules. Invoke it
explicitly with `$ai-humans-development`.

For a requested code review or an agreed review step,
[`ai-humans-code-review`](.agents/skills/ai-humans-code-review/SKILL.md) supplements
that workflow with review priorities, evidence, and findings ordered by severity.
Invoke it explicitly with `$ai-humans-code-review` to review current changes or
a specified area of the project.

Five local technical skills supplement that workflow:

| Skill | Use for |
| --- | --- |
| [`wagtail-content-modeling`](.agents/skills/wagtail-content-modeling/SKILL.md) | Page types, snippets, fields, StreamField, editor interfaces, and content migrations. |
| [`wagtail-backend`](.agents/skills/wagtail-backend/SKILL.md) | Queries, search, permissions, publishing, workflows, and runtime behavior. |
| [`wagtail-frontend`](.agents/skills/wagtail-frontend/SKILL.md) | Templates, accessibility, media, metadata, and editor previews. |
| [`wagtail-api`](.agents/skills/wagtail-api/SKILL.md) | API v3 configuration and integrations. |
| [`wagtail-upgrade`](.agents/skills/wagtail-upgrade/SKILL.md) | Wagtail upgrade planning and implementation. |

Use only the technical skills relevant to a task, following the configured
Docker, uv, and `just` workflow. References to linting or frontend builds apply
when those tools are configured. All seven skills are included in this project;
no source checkout or user-level installation is needed. They can evolve with
this site's own requirements. The imported skills' source commit, licence
material, and update guidance are recorded in
[the provenance notes](.agents/skills/PROVENANCE.md).

## Local development

Install Docker with Compose and just, then run from the project directory:

```sh
just setup
just superuser
```

Open http://localhost:8000/ and http://localhost:8000/admin/.
`just setup` builds the development image, starts PostgreSQL, applies migrations,
and starts the web service in the background. Python changes reload automatically.

```sh
just                       # List commands
just up                    # Start the local stack
just down                  # Stop, retaining database data
just status
just logs                  # Follow web logs
just logs db
just manage makemigrations
just migrate
just check
just test home --noinput
just lint                  # Check Python errors and import order
just format-check          # Check Python formatting without changes
just format                # Sort imports and format Python files
just shell                 # Open a shell in the running web container
just manage update_index
just manage shell
just dbshell
just rebuild               # Rebuild after Dockerfile or host uv changes
just manage-once check     # Temporary container; no running web service needed
```

`just add package-name` or `just add --dev package-name` updates dependencies and
the lockfile, then rebuilds/restarts locally. Commit both dependency files.
`just manage shell -c 'print("quoted arguments work")'` illustrates passing
quoted arguments. Most Django shortcuts use the running web container.

Use `just shell` for ad-hoc commands inside the running development web container.
It opens `/bin/sh` as the application user in `/app`, with the container's Python
environment on `PATH`. Type `exit` to return to your host terminal.
`just manage shell` opens the Django Python shell instead.

Development uses database/user `wagtail` and password `wagtail-dev-password`.
The database is private to the Compose network at `db:5432`; it has no host port.
Its data is kept in a named volume. Uploaded media stays in the source directory
at `media/`. The container environment is `/opt/venv`, separate from the host's
ignored `.venv`. `just down` retains volumes; Docker's `down --volumes` deletes
them. This project uses PostgreSQL, with no SQLite fallback.

### Python formatting and linting

[Ruff](https://docs.astral.sh/ruff/) provides Python formatting, linting, and
import sorting. Its version is pinned in the `dev` dependency group and locked
in `uv.lock`. It is installed in development images and excluded from production
dependencies. `just setup` builds the development image with Ruff installed;
after changing dependencies, use `just rebuild`.

Run `just lint` and `just format-check` before handing over Python changes.
Both commands report problems without modifying files. Use `just format` to sort
imports and apply formatting, then run both checks again. `just lint --fix`
applies Ruff's available safe lint fixes; review the resulting diff.

These commands use temporary development containers with the source directory
mounted, so they do not require a running web server or database. Formatting and
fixes update the files in your checkout. They supplement `just check` and the
relevant `just test` commands.

Configuration lives in `pyproject.toml`: Python __PYTHON_VERSION__, an 88-character
formatting target, basic Python error checks (`E4`, `E7`, `E9`, `F`), and import
sorting (`I`). The two environment settings modules allow their deliberate
wildcard imports; production also allows references to names supplied by that
import. Other checks still apply. Migrations retain Python error checks but are
excluded from formatting and import sorting. The `.agents` directory and paths
ignored by Git, such as local settings, uploaded media, collected static files,
and virtual environments, are excluded. HTML templates, CSS, JavaScript, and
Markdown are outside Ruff's scope.

## Site assets

Keep the site's CSS, JavaScript, and design images together in the project-level
`assets/` folder rather than adding static folders to individual application apps:

```text
assets/
├── css/
│   ├── site.css
│   └── welcome.css
├── js/
│   └── site.js
└── images/
```

`site.css` and `site.js` are loaded by the base template for shared styling and
browser behaviour. The homepage loads `welcome.css` for the starter welcome
screen. Add focused CSS or JavaScript files here when needed, and load them
through the templates' `extra_css` and `extra_js` blocks. Templates stay in their
existing locations. Wagtail and third-party packages retain their own assets.

These are ordinary CSS and JavaScript files with no compilation step. Django
finds them through `STATICFILES_DIRS`; refer to them with the `static` template
tag, for example `{% static 'css/site.css' %}`. The root `static/` folder is
generated by `collectstatic` for production and should not be edited. Uploaded
content belongs in `media/`, separately from these version-controlled site assets.

## Production Docker

The Dockerfile defaults to the production target. It uses Gunicorn on port 8000
as a non-root user, `config.settings.production` with `DEBUG=False`, and
WhiteNoise for collected static assets. Dependencies are installed from the
lockfile. The final image omits uv and compiler tools. Migrations run separately.

```sh
docker build --target production -t __SITE_SLUG__:production .
```

For an x86 host when building on Apple Silicon, add `--platform linux/amd64` or
let hosting build the image. Supply the runtime variables in
`.env.production.example` through the host's environment configuration.

The standalone `compose.production.yaml` is a single-server example. It uses
its own PostgreSQL and media volumes and no source bind mount. Do not merge it
with development Compose. When its hostnames, origins, and secrets are ready:

```sh
cp .env.production.example .env.production
# Generate independent Django/database secrets, then edit .env.production.
docker compose run --rm --no-deps web python -c "import secrets; print(secrets.token_urlsafe(64)); print(secrets.token_urlsafe(32))"
just prod-build
just prod-migrate
just prod-manage createsuperuser
just prod-up
just prod-logs
```

Keep secret values single-quoted in the environment file so Compose preserves
dollar signs. Database environment variables initialize a new data volume;
changing a password later also requires updating the existing PostgreSQL role.

Production and development use host port 8000 in their separate Compose
examples. Stop development before testing production on that same port. These
commands use the Docker host selected by your current Docker context.

Configure HTTPS and trusted proxy handling, secure cookies, upload delivery,
outbound email, and database/media backups for the chosen hosting provider.
WhiteNoise serves static assets, not uploaded media; use a proxy or object
storage for uploads. For a managed PostgreSQL service, supply its connection
variables and TLS settings to the application image instead of using the
bundled database. Run `python manage.py check --deploy` in the real hosting
environment before launch. Plan PostgreSQL major upgrades separately.
