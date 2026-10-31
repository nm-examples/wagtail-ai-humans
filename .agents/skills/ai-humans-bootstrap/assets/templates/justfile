# Forward arguments through the shell without losing quoting or spaces.
set positional-arguments

compose := "docker compose -f compose.yaml"
production := "docker compose --env-file .env.production -f compose.production.yaml"

# List the available commands.
default:
    @just --list

# Build, migrate, and start the local development stack.
setup: build
    {{ compose }} run --rm web python manage.py migrate
    {{ compose }} up -d

# Build the development image; accepts Compose build flags.
build *args:
    {{ compose }} build "$@"

# Start the local stack in the background; accepts Compose up flags.
up *args:
    {{ compose }} up -d "$@"

# Stop the local stack, keeping database data.
down:
    {{ compose }} down

# Show container status.
status:
    {{ compose }} ps

# Follow application logs, or specify other services such as db.
logs *args="web":
    {{ compose }} logs --follow "$@"

# Rebuild the development image and restart the local stack.
rebuild:
    {{ compose }} up --build -d

# Run a Django management command in the running development container.
manage +args:
    {{ compose }} exec web python manage.py "$@"

# Run a Django command in a temporary container, starting the database if needed.
manage-once +args:
    {{ compose }} run --rm web python manage.py "$@"

# Apply local database migrations; accepts migrate options.
migrate *args:
    {{ compose }} exec web python manage.py migrate "$@"

# Create a local admin account interactively.
superuser *args:
    {{ compose }} exec web python manage.py createsuperuser "$@"

# Run Django system checks.
check *args:
    {{ compose }} exec web python manage.py check "$@"

# Run Django tests; accepts test labels and options.
test *args:
    {{ compose }} exec web python manage.py test "$@"

# Add Python dependencies (optionally --dev), then rebuild and restart locally.
add +args:
    {{ compose }} run --rm --no-deps web uv add "$@"
    {{ compose }} up --build -d

# Open the local PostgreSQL SQL prompt.
dbshell:
    {{ compose }} exec db psql -U wagtail -d wagtail

# Build the production image using .env.production.
prod-build:
    {{ production }} build

# Start the production stack using .env.production.
prod-up:
    {{ production }} up -d

# Follow production application logs, or specify other services.
prod-logs *args="web":
    {{ production }} logs --follow "$@"

# Apply production migrations as an explicit release command.
prod-migrate *args:
    {{ production }} run --rm web python manage.py migrate "$@"

# Run a production Django command in a temporary container.
prod-manage +args:
    {{ production }} run --rm web python manage.py "$@"
