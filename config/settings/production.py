from .base import *

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ["hands.n-e.kr"]
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME_PRODUCTION"),
        "USER": env("DB_USER_PRODUCTION"),
        "PASSWORD": env("DB_PASSWORD_PRODUCTION"),
        "HOST": env("DB_HOST_PRODUCTION"),
        "PORT": env("DB_PORT_PRODUCTION"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True