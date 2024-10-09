"""
Django settings for Aula project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    # extra
    "dashboard",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django_browser_reload",
    "tailwind",
    "theme",
    "rest_framework",
    "rest_framework_simplejwt",
    # ------
    "home",
    "search",
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.settings",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps
    "base",
    "usuarios",
    "programa_startup",
    # ------
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "Aula.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.csrf",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "Aula.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SENDGRID_API_KEY = (
    "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"
)
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "es"

LANGUAGES = [
    ("en", ("English")),
    ("es", ("Spanish")),
]

TIME_ZONE = "America/Lima"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
    os.path.join(BASE_DIR, "theme", "static_src"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}


# Wagtail settings

WAGTAIL_SITE_NAME = "Aula"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "AUTO_UPDATE": False,
    }
}

ATOMIC_REBUILD = True

WAGTAILSEARCH_HITS_MAX_AGE = 7

WAGTAIL_I18N_ENABLED = True

LANGUAGES = [
    ("en", ("English (United Kingdom)")),
    ("en-us", ("English (United States)")),
    ("es", ("Spanish (Spain)")),
    ("es-mx", ("Spanish (Mexico)")),
]


WAGTAIL_CONTENT_LANGUAGES = [
    ("en", ("English")),
    ("es", ("Spanish")),
]

WAGTAILEMBEDS_RESPONSIVE_HTML = True
WAGTAILADMIN_RECENT_EDITS_LIMIT = 5
# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://127.0.0.1:800"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

# Customize the behavior of rich text fields. By default, RichTextField and RichTextBlock use the configuration given under
# the 'default' key, but this can be overridden on a per-field basis through the editor keyword argument,
# for example body = RichTextField(editor='secondary').
# See: https://docs.wagtail.org/en/stable/reference/settings.html
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {"features": ["h2", "bold", "italic", "link", "document-link"]},
    },
    "secondary": {
        "WIDGET": "some.external.RichTextEditor",
    },
}

WAGTAILADMIN_EXTERNAL_LINK_CONVERSION = "all"

WAGTAILADMIN_COMMENTS_ENABLED = False

WAGTAIL_AUTO_UPDATE_PREVIEW = True

WAGTAIL_AUTO_UPDATE_PREVIEW_INTERVAL = 500

WAGTAILADMIN_UNSAFE_PAGE_DELETION_LIMIT = 20

WAGTAIL_ENABLE_UPDATE_CHECK = True

WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False

WAGTAIL_ENABLE_WHATS_NEW_BANNER = True

WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = False

WAGTAILFORMS_HELP_TEXT_ALLOW_HTML = True

WAGTAIL_WORKFLOW_CANCEL_ON_PUBLISH = False

# ----------TAILWIND----------
TAILWIND_APP_NAME = "theme"
TAILWIND_CSS_PATH = "css/dist/styles.css"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = [
    "127.0.0.1",
]

# --------------REST FRAMEWORK----------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# ----------------JWT---------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "ES256",
    "SIGNING_KEY": "MHQCAQEEIDr6j/NdnM7Xe5iBJLIKJb17czUg67ZqxbWfoF31FlvaoAcGBSuBBAAKoUQDQgAEI+sea7S3wKqfIP65x7KvP3naESVkufmkAtpAmBUoPT5WHB2ThsRCm+l5IP8KKz7E+KHWPAaLLsAMgE3FKAqGcg==",
    "VERIFYING_KEY": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEI+sea7S3wKqfIP65x7KvP3naESVkufmkAtpAmBUoPT5WHB2ThsRCm+l5IP8KKz7E+KHWPAaLLsAMgE3FKAqGcg==",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(minutes=1),
}
# -----------------------SESSIONS--------------------------------

AUTHENTICATION_BACKENDS = [
    "usuarios.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AUTH_USER_MODEL = "usuarios.CustomUser"
LOGIN_REDIRECT_URL = "/"
SESSION_COOKIE_SECURE = True  # Solo para HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies
SESSION_COOKIE_HTTPONLY = True

# -----------------Node-----------------------------------
NPM_BIN_PATH = "npm.cmd"
