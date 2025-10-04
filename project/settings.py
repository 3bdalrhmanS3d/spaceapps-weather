from pathlib import Path
import os
from urllib.parse import urlparse, parse_qs
import dj_database_url  # <= لو ركّبتها

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-k@331c-cmusd@+=ey6tbo$%rzmul%hk1j3*n2q%#hh+@$0aw7p'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',

    # Local apps
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # يجب أن يكون أول ميدلوير تقريبًا
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'

def database_from_url(url: str):
    r = urlparse(url); qs = parse_qs(r.query)
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': r.path.lstrip('/'),
        'USER': r.username,
        'PASSWORD': r.password,
        'HOST': r.hostname,
        'PORT': r.port or 5432,
        'OPTIONS': {
            'sslmode': qs.get('sslmode', ['prefer'])[0],
            'connect_timeout': int(qs.get('connect_timeout', [10])[0]),
        },
        'CONN_MAX_AGE': 600,
    }

DATABASES = {
"default": dj_database_url.parse(
os.environ.get(
"DATABASE_URL",
# fallback to your Neon URL if env var is missing
"postgresql://neondb_owner:npg_el8ACGstZOg0@ep-young-smoke-adff87p9-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require",
),
conn_max_age=600,
ssl_require=True,
)
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {'TITLE': 'SpaceApps Weather Probability API', 'VERSION': '1.0.0'}
CORS_ALLOW_ALL_ORIGINS = True
