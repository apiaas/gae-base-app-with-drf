import logging
from rest_framework import authentication


class QuietBasicAuthentication(authentication.BasicAuthentication):
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm


class CSRFExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        msg = '{} user authenticated through CSRF exempt session auth.'
        logging.info(msg.format(unicode(request.user)))
