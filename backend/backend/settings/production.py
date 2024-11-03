from pathlib import Path
from datetime import timedelta
from decouple import config


# TODO: Defende against shell uploading
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("PRODUCTION_SECRET_KEY")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party app
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',

    # Local app
    'user.apps.UserConfig',
    'project.apps.ProjectConfig',
    'dash_board.apps.DashBoardConfig',
    'club.apps.ClubConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# TODO: Change the default port to something else
ALLOWED_HOSTS = ["http://192.168.1.51:8080", "prometheus"]


# TODO : Rest framework configurations
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}


# TODO: Make sure about SSL connection
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': config('DB_NAME'),
    'USER': config('DB_USER'),
    'HOST': config('DB_HOST'),
    'PASSWORD': config('DB_PASSWORD'),
    'OPTIONS': {
        'sslmode': 'require'
        },
    }
}


# TODO: Collect the caches into Redis
CACHES = {
'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': '127.0.0.1:6379/1',
    }
}


# TODO: JWT Authentication
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True


# TODO: Ensure HTTPS is used
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# TODO: JWT settings for better security
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


# TODO: CORS settings if your API is accessed from different domains
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True


# TODO: Prometheus settings
PROMETHEUS_LATENCY_BUCKETS = (0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 25.0, 50.0, 75.0, float("inf"),)
PROMETHEUS_METRIC_NAMESPACE = "config"


# TODO: Log everything :))
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}',
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "special": {
            "()": "project.logging.SpecialFilter",
            "foo": "bar",
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",  # Log warnings and above to console
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",  # Log info and above to file
            "class": "logging.FileHandler",
            # TODO: Make sure about path in Production mode
            "filename": "/path/to/your/project/logs/django_info.log",
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",  # Log errors to a separate file
            "class": "logging.FileHandler",
            # TODO: Make sure about path in Production mode
            "filename": "/path/to/your/project/logs/django_error.log",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",  # Send error logs via email
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["special"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",  # Log info and above
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",  # Log errors in requests
            "propagate": False,
        },
        "backend.custom": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",  # Log info and above from your custom logger
            "filters": ["special"],
        },
    },
}
