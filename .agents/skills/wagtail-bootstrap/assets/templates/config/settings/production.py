import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]
if not SECRET_KEY or not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "Production requires DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS."
    )

if any(
    not os.environ.get(variable)
    for variable in ("POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST")
):
    raise ImproperlyConfigured(
        "Production requires POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, "
        "and POSTGRES_HOST."
    )

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "")

# Persist uploads outside the container's writable layer.
MEDIA_ROOT = Path(os.environ.get("DJANGO_MEDIA_ROOT", "/data/media"))

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES["staticfiles"]["BACKEND"] = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

SECURE_SSL_REDIRECT = (
    os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "false").lower() == "true"
)
SESSION_COOKIE_SECURE = (
    os.environ.get("DJANGO_SESSION_COOKIE_SECURE", "false").lower() == "true"
)
CSRF_COOKIE_SECURE = (
    os.environ.get("DJANGO_CSRF_COOKIE_SECURE", "false").lower() == "true"
)
if os.environ.get("DJANGO_TRUST_X_FORWARDED_PROTO", "false").lower() == "true":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
