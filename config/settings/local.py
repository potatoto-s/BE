from .base import *

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ["*"]
DEBUG = True

# 미디어 파일 설정 추가
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3.local",
    }
}
