# Wagtail AI Humans

Wagtail CMS with Python 3.14, PostgreSQL 18, and dependencies managed by uv. Docker Compose is
the main local development workflow. Docker's default build target is a separate
production image.

This repository includes seven local skills. Two define the project workflow:

- [`wagtail-development`](.agents/skills/wagtail-development/SKILL.md) guides
  ongoing application work and owns the shared development, Git, and pull-request
  rules. Invoke it with `$wagtail-development`; [AGENTS.md](AGENTS.md) also directs
  agents to use it for application development and review.
- [`wagtail-bootstrap`](.agents/skills/wagtail-bootstrap/SKILL.md) includes its
  own templates for creating another site. Invoke it with `$wagtail-bootstrap`
  and supply the new project directory and site name.

Five imported skills provide technical guidance alongside `wagtail-development`:

| Skill | Use for |
| --- | --- |
| [`wagtail-content-modeling`](.agents/skills/wagtail-content-modeling/SKILL.md) | Page types, snippets, fields, StreamField, editor interfaces, and content migrations. |
| [`wagtail-backend`](.agents/skills/wagtail-backend/SKILL.md) | Queries, search, permissions, publishing, workflows, and runtime behavior. |
| [`wagtail-frontend`](.agents/skills/wagtail-frontend/SKILL.md) | Templates, accessibility, media, metadata, and editor previews. |
| [`wagtail-api`](.agents/skills/wagtail-api/SKILL.md) | API v3 configuration and integrations. |
| [`wagtail-upgrade`](.agents/skills/wagtail-upgrade/SKILL.md) | Wagtail upgrade planning and implementation. |

Use only the technical skills relevant to a task. The development skill continues
to govern scope, project conventions, verification, Git, and pull requests. Use
the configured Docker, uv, and `just` workflow when applying technical guidance;
references to linting or frontend builds apply when those tools are configured.

The imported directories are version-controlled copies. Their
[provenance and update notes](.agents/skills/PROVENANCE.md) record the source
commit, preserved licence material, and update process. They are included only
in this application, with no dependency on a sibling checkout.

## Project folders

Work on this project spans two sibling repositories:

- `wagtail-ai-humans/`: the Wagtail application and its repository skills.
- `../wagtail-ai-humans-base/`: the reusable copies of `wagtail-development`,
  `wagtail-bootstrap`, and bootstrap resources.

When updating either workflow skill, copy the complete update to the matching
directory in `wagtail-ai-humans-base`, including templates, references, UI
metadata, and resource additions or removals. When changing `wagtail-development`,
also update its bundled copy at
`.agents/skills/wagtail-bootstrap/assets/templates/.agents/skills/wagtail-development/`
before mirroring the bootstrap skill. Preserve unrelated application changes and
independent edits in either repository.

Both repositories have their own `AGENTS.md` appropriate to their role. Bootstrap
templates include project instructions and the development skill so new sites
carry the workflow independently. Generated sites do not inherit the source
repositories' sibling-mirroring requirements or the bootstrap skill itself.

The five imported technical skills are not currently mirrored into the base
repository or included in bootstrap templates.

## Local development

Install Docker with Compose and [just](https://just.systems/). On macOS, install
just with `brew install just`. Run these commands from the project directory:

```sh
just setup
just superuser
```

`just setup` builds the image, starts PostgreSQL, applies migrations, and starts
the web server in the background. On subsequent visits, use `just up`.
Run `just` or `just --list` to see the documented shortcuts. Commands also work
from project subdirectories.

Open http://localhost:8000 and http://localhost:8000/admin/. Python edits trigger
Django's automatic reload. Templates and static files are read from the mounted
source directory. PostgreSQL data stays in a Docker named volume, and uploaded
files (`media/`) stay in the project directory when containers are removed.
Compose waits for PostgreSQL's health check before starting Django. The database
is available to containers as `db:5432` and is not published on the host.

Development uses database/user `wagtail` and password `wagtail-dev-password`.
These are local development credentials only. Production requires its own
database password. Django uses Psycopg 3 through the `psycopg[binary]` dependency.

The container uses its own Linux environment at `/opt/venv`; the Mac's `.venv`
is not used. The development target includes uv and any development dependency
groups. It does not run `collectstatic` or migrations at startup.

Stop and remove containers with `just down`; the database volume survives.
Using Docker's `down --volumes` deletes the database.

### Common commands

```sh
just up                         # Start in the background
just down                       # Stop, keeping database data
just status                     # Show container status
just logs                       # Follow application logs (Ctrl+C to stop following)
just logs db                    # Follow PostgreSQL logs
just rebuild                    # Rebuild and restart after Dockerfile changes

just manage makemigrations
just migrate
just check
just test
just test home --keepdb
just manage shell
just manage shell -c 'print("hello from Django")'
just dbshell

# Add dependencies, update pyproject.toml and uv.lock, then rebuild and restart.
just add django-debug-toolbar
just add --dev ruff

# Run Django commands without an already-running web container.
just manage-once check
```

`manage`, `migrate`, `superuser`, `check`, and `test` use the running web container.
`manage-once` starts a temporary container and the database if needed. Arguments,
including quoted Python code, are forwarded as supplied. The shortcuts explicitly
select the development Compose file; production shortcuts begin with `prod-`.
The underlying Docker Compose commands remain available if you need them.

Alternatively, host-installed uv can update dependencies with `uv add`.
Commit both `pyproject.toml` and `uv.lock`. Image builds use `uv sync --locked`,
so an out-of-date lockfile fails the build. Run `just rebuild` after changing
dependencies with host-installed uv.

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
existing locations.

These are ordinary CSS and JavaScript files with no compilation step. Django
finds them through `STATICFILES_DIRS`; refer to them with the `static` template
tag, for example `{% static 'css/site.css' %}`. The root `static/` folder is
generated by `collectstatic` for production and should not be edited. Uploaded
content belongs in `media/`, separately from these version-controlled site assets.

## Production Docker

The `production` target runs Gunicorn as the unprivileged `wagtail` user with
`config.settings.production` and `DEBUG=False`. It installs only locked runtime
dependencies and collects versioned static assets at build time. WhiteNoise
serves those assets, including Wagtail's admin CSS and JavaScript. Source code is
copied into the image, rather than mounted from the host. uv and build tools are
left out of the final image.

Build the production image:

```sh
docker build --target production -t wagtail-ai-humans .
```

When building on Apple Silicon for an x86 server, add `--platform linux/amd64`,
or let the hosting platform build the image from this repository.

The container listens on port 8000. Supply environment variables through the
hosting platform using `.env.production.example` as the reference. A secret key
and allowed hostnames are required at runtime, along with `POSTGRES_DB`,
`POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_HOST`. Set `POSTGRES_PORT`
and `POSTGRES_SSLMODE` as needed by the database provider. The build-only
placeholders do not become runtime credentials, and image builds do not need a
running database. Set `WAGTAILADMIN_BASE_URL` and trusted CSRF origins to the
site's HTTPS origin.

### Single-server Compose example

`compose.production.yaml` is a standalone file. Do not merge it with
`compose.yaml`, which mounts development source code. The production example
uses a separate Compose project, a PostgreSQL service, and separate named volumes
for database data and uploaded media. The database port is not published.

```sh
cp .env.production.example .env.production
# Generate a Django key and a separate database password; put them and your
# hostnames in .env.production. No development database is needed for this.
docker compose run --rm --no-deps web python -c "import secrets; print(secrets.token_urlsafe(64)); print(secrets.token_urlsafe(32))"

just prod-build
just prod-migrate
just prod-manage createsuperuser
just prod-up
```

Production shortcuts select `compose.production.yaml` and pass
`--env-file .env.production`. Use `just prod-logs` to follow application logs.
They operate on the Docker host selected by your current Docker context.

Keep secrets inside single quotes in `.env.production`, as in the example, so
Compose does not interpret dollar signs. Passing `--env-file` supplies the
database credentials to both services. These variables only initialize a new
PostgreSQL data volume; changing the password later also requires updating the
existing PostgreSQL role.

The development and production examples both bind host port 8000 to loopback;
stop the development stack before starting this production example locally.

### Hosting integration

- Run migrations explicitly as a release command before starting an updated
  application. They never run automatically in the web container's command.
- Configure HTTPS at the hosting reverse proxy. Once enabled, set
  `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_SESSION_COOKIE_SECURE`, and
  `DJANGO_CSRF_COOKIE_SECURE` to `true`. Enable
  `DJANGO_TRUST_X_FORWARDED_PROTO` only if that trusted proxy strips incoming
  `X-Forwarded-Proto` headers and sets the correct value itself.
- WhiteNoise serves static assets, not uploads. Configure the hosting proxy to
  serve `/media/` from the persistent media directory, or configure object storage
  when the hosting provider is chosen. Keep uploaded content on a separate
  origin where possible. Wagtail's protected document URLs still use Django.
- Keep PostgreSQL and uploaded media on persistent storage and back up both.
  PostgreSQL 18's volume is mounted at `/var/lib/postgresql`, with its
  version-specific data directory underneath. Plan major database upgrades
  separately; changing the image's major version is not a data migration.
  Do not use `docker compose down --volumes` on production unless you intend to
  delete that data. For multiple application replicas, use shared media storage.
  A managed PostgreSQL service can replace the bundled database when the hosting
  provider is chosen; supply its connection variables to the application image.
- Configure production email through the chosen provider before relying on
  password reset or notification emails.
- Run `python manage.py check --deploy` with the real deployment environment
  before launch. HTTPS, media delivery, email, and database services remain
  hosting-specific configuration.

For later deployments, rebuild or pull the image, run the migration release
command, then recreate the web service. Back up the database before migrations.
