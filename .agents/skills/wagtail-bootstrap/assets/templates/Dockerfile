# Shared Python and runtime libraries for both environments.
FROM python:__PYTHON_VERSION__-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libjpeg62-turbo \
    libwebp7 \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 wagtail \
 && mkdir -p /app /data/media \
 && chown -R wagtail:wagtail /app /data

WORKDIR /app
EXPOSE 8000


# Build dependencies once, separately from the application source.
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:__UV_VERSION__ /uv /usr/local/bin/uv

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project


# Compose selects this target for local development.
FROM builder AS development

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project \
 && chown -R wagtail:wagtail /opt/venv

COPY --chown=wagtail:wagtail . .
ENV DJANGO_SETTINGS_MODULE=config.settings.dev
USER wagtail

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# The default image is the production image, with no source bind mount or uv.
FROM base AS production

ENV DJANGO_SETTINGS_MODULE=config.settings.production

COPY --from=builder /opt/venv /opt/venv
COPY --chown=wagtail:wagtail . .
USER wagtail

# These values only apply to asset collection; runtime secrets come from hosting.
RUN DJANGO_SECRET_KEY=build-only-placeholder \
    DJANGO_ALLOWED_HOSTS=localhost \
    POSTGRES_DB=build-only \
    POSTGRES_USER=build-only \
    POSTGRES_PASSWORD=build-only \
    POSTGRES_HOST=localhost \
    python manage.py collectstatic --noinput --clear

# Run migrations as a separate release command before starting new containers.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "config.wsgi:application"]
