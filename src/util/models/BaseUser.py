from google.appengine.ext import ndb
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable
)
from django.utils.crypto import salted_hmac

from util.models import BaseModel


class BaseUser(BaseModel):
    """
    This model is inspired by Django's AbstractBaseUser model.
    """
    email = ndb.StringProperty(required=True)
    password_hash = ndb.StringProperty()
    active = ndb.BooleanProperty(default=True)

    last_login = ndb.DateTimeProperty()

    @classmethod
    def get_by_email(cls, email):
        return cls.all().filter(cls.email == str(email).lower()).get()

    def id(self):
        return self.key.id()

    @property
    def pk(self):
        """
        Some Django functionality assumes users have pk field.
        """
        return self.key.id()

    def save(self, *args, **kwargs):
        """
        Delegate any user.save() calls to put()
        """
        self.put()

    def get_username(self):
        return self.email

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @property
    def is_active(self):
        return self.active

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        return check_password(raw_password, self.password_hash)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password_hash = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password_hash)

    def get_full_name(self):
        raise NotImplementedError('subclasses of BaseUser must provide a get_full_name() method')

    def get_short_name(self):
        raise NotImplementedError('subclasses of BaseUser must provide a get_short_name() method.')

    def get_session_auth_hash(self):
        """
        Returns an HMAC of the password field.
        """
        # This can be any string. It is added to the secret key from settings.
        key_salt = "models.ndb.BaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password_hash).hexdigest()