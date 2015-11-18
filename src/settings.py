import os
pdir = os.path.dirname

BASE_DIR = pdir(__file__)

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'landing',
)

MIDDLEWARE_CLASSES = (
    # NdbDjangoMiddleware tells the ndb handler not to exit until its
    # asynchronous requests have finished (same as ndb.toplevel decorator).
    'google.appengine.ext.ndb.django_middleware.NdbDjangoMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'landing', 'templates'),
)

# only use the memory file uploader, do not use the file system - not able to do so on
# google app engine
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler',)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'main.application'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTHENTICATION_BACKENDS = ('backends.auth.ModelBackend', )
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

SECRET_KEY = '#62483%e^vp-=w0sd4sxem1%tdu@6(YDu%r@ff=$84l27wi%vd'
