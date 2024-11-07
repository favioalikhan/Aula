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
import dj_database_url
SECRET_KEY = os.environ.get('SECRET_KEY', default='rnd_0gLkWCpcbozmlRvy7XUHLQt0OybX')

# from datetime import timedelta
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    # extra
    #"usuarios",
    # "usuarios.apps.UsuariosConfig",
    # "usuarios.apps.CustomWagtailUsersConfig",
    "dashboard",
    # "modeltranslation",
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
    # "rest_framework",
    # "rest_framework_simplejwt",
    "home",
    "search",
    # "usuarios.apps.UsuariosConfig",
    # ------------
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.settings",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    # "usuarios.apps.CustomWagtailUsersConfig",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cleanup.apps.CleanupConfig",
    "whitenoise.runserver_nostatic",
    # "debug_toolbar",
    "import_export",
    "guardian",
    "simple_history",
    "django_celery_beat",
    "djmoney",
    # ------
    # ------ Apps
    "usuarios",
    "Aula",
    "base",
    "programa_startup",
]
WAGTAIL_ADMIN_BASE_URL = None

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # "simple_history.middleware.HistoryRequestMiddleware",
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
    # "default": {
    #    "ENGINE": "django.db.backends.sqlite3",
    #   "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    # }
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'aula',
    #    'USER': 'postgres',
    #    'PASSWORD': '9870',
    #    'HOST': 'localhost',  # o la dirección de tu servidor PostgreSQL
    #    'PORT': '5432',       # el puerto de PostgreSQL, por defecto es 5432
    #}
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

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

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    
LOGIN_URL = "login"
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
    # "django.contrib.staticfiles.finders.FileSystemFinder",  # Activar esta línea en caso de tener la advertencia:Found another file with the destination path '/path'  It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
    # "Aula.custom_finders.CustomAppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
    os.path.join(BASE_DIR, "theme", "static_src"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

DEBUG = 'RENDER' not in os.environ

if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

######################################################################
# Unfold
######################################################################

UNFOLD = {
    "SITE_HEADER": _("Aula Admin"),
    "SITE_TITLE": _("Aula Admin"),
    "SITE_SYMBOL": "settings",
    # "SHOW_HISTORY": True,
    "ENVIRONMENT": "Aula.utils.environment_callback",
    "DASHBOARD_CALLBACK": "Aula.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("aula/img/incuval-admin.png"),
    },
    # "STYLES": [
    # lambda request: static("css/dist/styles.css"),
    # ],
    # "SCRIPTS": [
    # lambda request: static("js/chart.min.js"),
    # ],
    "TABS": [
        {
            "models": ["usuarios.CustomUser", "auth.group"],
            "items": [
                {
                    "title": _("Users"),
                    "icon": "person",
                    "link": reverse_lazy("aula_admin:usuarios_customuser_changelist"),
                },
                {
                    "title": _("Groups"),
                    "icon": "group",
                    "link": reverse_lazy("aula_admin:auth_group_changelist"),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                # "title": _("Navigation"),
                # "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("aula_admin:index"),
                    },
                ],
            },
            {
                "title": _("Usuarios y Grupos"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy(
                            "aula_admin:usuarios_customuser_changelist"
                        ),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("aula_admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Emprendedores"),
                        "icon": "business",
                        "link": reverse_lazy(
                            "aula_admin:usuarios_emprendedor_changelist"
                        ),
                    },
                    {
                        "title": _("Mentores"),
                        "icon": "supervisor_account",
                        "link": reverse_lazy("aula_admin:usuarios_mentor_changelist"),
                    },
                ],
            },
            {
                "items": [
                    {
                        "title": _("Mentorías"),
                        "icon": "question_answer",
                        "link": reverse_lazy("aula_admin:usuarios_mentoria_changelist"),
                    }
                ]
            },
            {
                "items": [
                    {
                        "title": _("Startups"),
                        "icon": "rocket",
                        "link": reverse_lazy(
                            "aula_admin:programa_startup_startup_changelist"
                        ),
                    }
                ]
            },
            {
                "items": [
                    {
                        "title": _("Entregables"),
                        "icon": "Package",
                        "link": reverse_lazy(
                            "aula_admin:programa_startup_tarea_changelist"
                        ),
                    }
                ]
            },
            {
                "items": [
                    {
                        "title": _("Tareas"),
                        "icon": "Task",
                        "link": reverse_lazy(
                            "aula_admin:programa_startup_entregable_changelist"
                        ),
                    }
                ]
            },
            {
                "title": _("Gestión de contenido CMS"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Editor de contenido"),
                        "icon": "edit",
                        "link": reverse_lazy("wagtailadmin_home"),
                    },
                    {
                        "title": _("Documentos"),
                        "icon": "folder",
                        "link": reverse_lazy("wagtaildocs:index"),
                    },
                ],
            },
        ],
    },
}

######################################################################
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
WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"

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
"""
# --------------REST FRAMEWORK----------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# ----------------JWT-----------------UTILIZAR A FUTURO----

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
"""
# -----------------------SESSIONS--------------------------------

AUTHENTICATION_BACKENDS = [
    "usuarios.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]
AUTH_USER_MODEL = "usuarios.CustomUser"
LOGIN_REDIRECT_URL = "/"
SESSION_COOKIE_SECURE = True  # Solo para HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies
SESSION_COOKIE_HTTPONLY = True

# -----------------Node-----------------------------------
NPM_BIN_PATH = "npm.cmd"
# -----------------Seguridad --------------------------------
# Seguridad HTTPS y SSL
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_SECONDS = 31536000  # 1 año
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_REDIRECT_EXEMPT = []
# SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
# SECURE_SSL_HOST = "mysecurehost.com"
# SECURE_SSL_REDIRECT = True

# Protección contra CSRF
# CSRF_COOKIE_DOMAIN = ".mydomain.com"
# CSRF_COOKIE_NAME = "csrftoken"
# CSRF_COOKIE_PATH = "/"
# CSRF_COOKIE_SAMESITE = "Strict"
# CSRF_COOKIE_SECURE = True
# CSRF_FAILURE_VIEW = "myapp.views.csrf_failure"
# CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"
# CSRF_TRUSTED_ORIGINS = ["https://mydomain.com", "https://subdomain.mydomain.com"]
# CSRF_USE_SESSIONS = True
# CSRF_COOKIE_HTTPONLY = False

# Secret Key
# SECRET_KEY = "my-very-secure-and-secret-key"
# SECRET_KEY_FALLBACKS = ["old-secret-key-1", "old-secret-key-2"]

# Otras configuraciones de seguridad
X_FRAME_OPTIONS = "DENY"
