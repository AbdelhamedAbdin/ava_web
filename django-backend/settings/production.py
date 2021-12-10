# from .base import *

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env("DEBUG")

# ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

# ####################### DON'T DUPLICATE APP #######################
# # DJANGO Project Apps Managments
# DJANGO_APPS += [

# ]

# THIRD_PARTY_APPS = [
#     'rest_framework_simplejwt.token_blacklist',
#     'rest_framework',
#     'corsheaders',
#     'djcelery_email',
# ]

# LOCAL_APPS = [
#     'authentication',
#     'quotations',
#     'clients',
#     'services',
#     'projects',
#     'invoices',
#     'receipts',
#     'expenses',
#     'lookups',
#     'firebase',
#     'emails'
# ]


# # INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS #(IF NO TENANCY)
# INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# ###################################################################

# # Database
# # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# DB_NAME = env("DB_NAME")
# DB_USER = env("DB_USER")
# DB_PASS = env("DB_PASS")
# DB_HOST = env("DB_HOST")
# DB_PORT = env("DB_PORT")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': DB_NAME,
#         'USER': DB_USER,
#         'PASSWORD': DB_PASS,
#         'HOST': DB_HOST,
#         'PORT': DB_PORT,
#     }
# }

#######################JWT TOKEN CUSTOMIZATION####################################
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': env("SECRET_KEY"),
#     'VERIFYING_KEY': None,
#     'AUTH_HEADER_TYPES': ('JWT',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
# }