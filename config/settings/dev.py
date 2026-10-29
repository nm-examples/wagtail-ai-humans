from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-prb)p+_fay*gw=c1bdck#^0oygbks-55wok7&1kz9jwble29po"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "web"]
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
