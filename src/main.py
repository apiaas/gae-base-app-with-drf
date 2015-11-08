import os

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.core import signals
from django.core.handlers.wsgi import WSGIHandler


def log_traceback(*args, **kwargs):
    import logging
    logging.exception("Exception in request:")

signals.got_request_exception.connect(log_traceback)

# Create a Django application for WSGI.
application = WSGIHandler()

# Add the staticfiles handler if necessary.
if settings.DEBUG and 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    from django.contrib.staticfiles.handlers import StaticFilesHandler
    application = StaticFilesHandler(application)

if getattr(settings, 'ENABLE_APPSTATS', False):
    from google.appengine.ext.appstats.recording import appstats_wsgi_middleware
    application = appstats_wsgi_middleware(application)
