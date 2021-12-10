from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

####################### DON'T DUPLICATE APP #######################
# DJANGO Project Apps Managments
DJANGO_APPS += [
    
]

THIRD_PARTY_APPS = [
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'corsheaders',
    'djcelery_email',
    # Oauth
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'rest_framework_social_oauth2',
    'django_filters'
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.clients',
    'apps.services',
    'apps.income',
    'apps.expenses',
    'apps.business',
    'apps.dashboards'
]


# INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS #(IF NO TENANCY)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
###################################################################
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
###################################################################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

# General Config For Social Accounts
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:8000/'
SOCIAL_AUTH_USER_FIELDS = ['email', 'username', 'first_name', 'password']

AUTHENTICATION_BACKENDS = (
    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
    # Apple OAuth2
    'social_core.backends.apple.AppleIdAuth',
    # rest_framework_social_oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # drf_social_oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)

DRFSO2_URL_NAMESPACE = 'drf'

# Facebook Configuration
SOCIAL_AUTH_FACEBOOK_KEY = env("FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = env("FACEBOOK_SECRET")

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Google Configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
   'https://www.googleapis.com/auth/userinfo.email',
   'https://www.googleapis.com/auth/userinfo.profile',
]

# Apple Configuration
SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True

SOCIAL_AUTH_APPLE_ID_CLIENT = ''
SOCIAL_AUTH_APPLE_ID_TEAM = ''
SOCIAL_AUTH_APPLE_ID_KEY = ''
SOCIAL_AUTH_APPLE_ID_SECRET = ""

ACTIVATE_JWT = True
###################################################################

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env("SECRET_KEY"),
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

###################################################################