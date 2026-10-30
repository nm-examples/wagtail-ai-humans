# __SITE_DISPLAY_NAME__

Wagtail CMS with Python __PYTHON_VERSION__, PostgreSQL __POSTGRES_MAJOR__, uv,
Docker Compose, and just. Dependencies are resolved for this site and recorded
in `pyproject.toml` and `uv.lock`.

## Development workflow

[AGENTS.md](AGENTS.md) directs application work to the repository-local
[`wagtail-development` skill](.agents/skills/wagtail-development/SKILL.md).
It covers focused scope, meaningful verification, and clear code review. Invoke
it explicitly with `$wagtail-development`. Both the instructions and skill are
included in this project; no source checkout or user-level installation is needed.
They can evolve with this site's own requirements.

## Local development

Install Docker with Compose and just, then run from the project directory:

```sh
just setup
just superuser
```

Open http://localhost:__HTTP_PORT__/ and http://localhost:__HTTP_PORT__/admin/.
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

Development uses database/user `wagtail` and password `wagtail-dev-password`.
The database is private to the Compose network at `db:5432`; it has no host port.
Its data is kept in a named volume. Uploaded media stays in the source directory
at `media/`. The container environment is `/opt/venv`, separate from the host's
ignored `.venv`. `just down` retains volumes; Docker's `down --volumes` deletes
them. This project uses PostgreSQL, with no SQLite fallback.

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

Production and development use host port __HTTP_PORT__ in their separate Compose
examples. Stop development before testing production on that same port. These
commands use the Docker host selected by your current Docker context.

Configure HTTPS and trusted proxy handling, secure cookies, upload delivery,
outbound email, and database/media backups for the chosen hosting provider.
WhiteNoise serves static assets, not uploaded media; use a proxy or object
storage for uploads. For a managed PostgreSQL service, supply its connection
variables and TLS settings to the application image instead of using the
bundled database. Run `python manage.py check --deploy` in the real hosting
environment before launch. Plan PostgreSQL major upgrades separately.
