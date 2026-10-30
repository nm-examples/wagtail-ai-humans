# Django configuration and bootstrap validation

Read this when applying the skill's templates to a newly generated Wagtail site.
Paths below are relative to that new project. Adapt to the generated template
and installed versions; do not assume line numbers or replace unrelated settings.

## Base and development settings

In `config/settings/base.py`, import `os` and replace the SQLite database setting:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "wagtail"),
        "USER": os.environ.get("POSTGRES_USER", "wagtail"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "wagtail-dev-password"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": {"sslmode": os.environ.get("POSTGRES_SSLMODE", "prefer")},
    }
}
```

Add `django.contrib.postgres` to `INSTALLED_APPS` if absent. Retain Wagtail's
generated database search configuration; PostgreSQL search fields and indexes
need the contrib app. Set `WAGTAIL_SITE_NAME` to the requested display name using
a properly escaped Python string literal.

In `config/settings/dev.py`, preserve its generated development secret key,
`DEBUG=True`, and console email backend. Set `ALLOWED_HOSTS` to
`["localhost", "127.0.0.1", "[::1]", "web"]`. Set `WAGTAILADMIN_BASE_URL` to
`http://localhost:<chosen-host-port>`.

The production settings template requires explicit credentials, uses
`config.settings.production` with `DEBUG=False`, and inserts WhiteNoise directly
after SecurityMiddleware. Keep static collection at build time; the build-only
placeholder values must not become runtime environment defaults.

## Public-site assets

Centralize the fresh scaffold's project-owned CSS, JavaScript, and design images
in root `assets/`. For the default `config` scaffold, move files as follows,
preserving their contents:

| Generated source | Destination |
| --- | --- |
| `config/static/css/config.css` | `assets/css/site.css` |
| `config/static/js/config.js` | `assets/js/site.js` |
| `home/static/css/welcome_page.css` | `assets/css/welcome.css` |

Inspect the actual generated scaffold and adapt these moves if its paths differ.
Keep an `assets/images/` directory for design images, using `.gitkeep` if empty.
Remove emptied project static directories; leave Wagtail and third-party package
assets in place. Do not replace the fresh welcome page or copy assets from the
source repository.

In `config/settings/base.py`, set `STATICFILES_DIRS = [BASE_DIR / "assets"]`.
Keep `STATIC_ROOT = BASE_DIR / "static"` as the separate production collection
destination and retain `AppDirectoriesFinder` for package assets. Update the
base template to load `css/site.css` and `js/site.js` with the `static` tag, and
the homepage's `extra_css` block to load `css/welcome.css`. Update any other
references affected by the moves. Templates stay in their generated locations.

Use ordinary CSS and JavaScript without adding compilation tooling. Shared
styling uses named CSS classes in separate stylesheets; focused files can be
added within the central folders and loaded through `extra_css` or `extra_js`.
Uploaded content stays in `media/`, outside the version-controlled design assets.
The bundled README documents this layout for the generated site's developers.

## Configuration invariants

- PostgreSQL and web credentials match within each Compose stack. Development
  credentials are local defaults; production requires its own password.
- The host virtual environment is ignored. The Linux environment stays at
  `/opt/venv`, outside the source mount at `/app`.
- The production target is the Dockerfile's default target. It contains locked
  runtime dependencies, no uv or compiler tools, and runs as a non-root user.
- Development and production Compose files are standalone. Production has no
  source bind mount and uses its own project name and volumes.
- PostgreSQL has a health check and web waits for readiness. The database port
  is private to the Compose network. For PostgreSQL 18+, use the volume mount at
  `/var/lib/postgresql`; PostgreSQL 17 uses `/var/lib/postgresql/data` instead.
  Adjust the template if explicitly selecting an older supported major.
- Migrations are explicit. Never delete a volume or existing database to make a
  bootstrap check pass. Never transfer data from the source repository.
- Only host HTTP port bindings and development URLs use the chosen host port;
  Django and Gunicorn listen on port 8000 inside the container.
- The Justfile keeps local commands on `compose.yaml`, and `prod-` commands use
  the production file and `.env.production`. Keep positional argument forwarding.
- Secret files, local settings, uploaded data, and caches stay out of Git and
  Docker build contexts.

## Validate the generated project

Check that `AGENTS.md` links to the included
`.agents/skills/wagtail-development/SKILL.md`, that the skill includes its
`agents/openai.yaml`, and that the README links resolve locally. The generated
guidance must not reference source repository paths or sibling mirroring. Validate
the included development skill with the skill validator when available.

Run from the new project, using its distinct Compose project name. If its
directory basename would reuse another site's resources, set a distinct name in
`compose.yaml` or use `COMPOSE_PROJECT_NAME` consistently for that new stack.

```sh
just --fmt --check
docker compose config --quiet
just setup
just check
just manage update_index
just test home --noinput
just manage shell -c 'print("quoted arguments work")'
just status
docker build --target production -t <site-slug>:production .
```

Verify the actual selected database backend and connectivity, not only that
settings load. Confirm the home page, admin login, search, and static assets
respond over HTTP. Confirm the rendered home page references `css/site.css`,
`css/welcome.css`, and `js/site.js`, and each URL serves the corresponding file.
Check in the browser that the welcome page retains its appearance. Verify the
production image collects and serves these assets through its manifest storage;
a successful build alone does not establish that they are reachable.
Touch a generated Python file without changing its content
and verify Django reports a reload and continues serving requests. Check that
PostgreSQL data survives recreation of its container using the new stack's own
volume. Leave the user's other projects and services running.

Validate production Compose using a temporary, isolated environment and project
when possible. Test authentication, migrations, Gunicorn/static serving, and
persistent storage; use a free host port. Clean up only resources created for
that test. The production environment example intentionally has blank secrets:
never replace it with test values or require real production secrets to test.

If Docker is unavailable, perform dependency, settings, formatting, and static
Compose checks where possible and report the runtime validation gap explicitly.
Do not create an admin with invented credentials; supply the interactive command.
