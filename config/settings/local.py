from .base import *

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ["hands.p-e.kr", "127.0.0.1", "211.188.63.3"]
DEBUG = True

# 미디어 파일 설정 추가
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME_LOCAL"),
        "USER": env("DB_USER_LOCAL"),
        "PASSWORD": env("DB_PASSWORD_LOCAL"),
        "HOST": env("DB_HOST_LOCAL"),
        "PORT": env("DB_PORT_LOCAL"),
        "OPTIONS": {
            "options": "-c search_path=handlocal",
        },
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
