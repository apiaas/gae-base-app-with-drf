from google.appengine.ext import ndb
from django.utils.translation import ugettext_lazy as _
from django.utils import six

from rest_framework import serializers


class KeyField(serializers.Field):
    default_error_messages = {
        'invalid': _('A valid identifier is required.'),
        'max_string_length': _('String value too large.')
    }
    MAX_STRING_LENGTH = 1000  # Guard against malicious string inputs.

    def __init__(self, **kwargs):

        self.entity_name = kwargs.pop('entity_name', None)
        self.entity_namespace = kwargs.pop('entity_namespace', '')
        self.entity_parent = kwargs.pop('entity_parent', None)
        self.id_type = kwargs.pop('id_type', int)
        super(KeyField, self).__init__(**kwargs)

        assert self.entity_name is not None, '`entity_name` is a required argument.'

    def to_internal_value(self, data):
        if isinstance(data, six.text_type) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            data = self.id_type(data)
        except (ValueError, TypeError):
            self.fail('invalid')

        return ndb.Key(
            self.entity_name, data, namespace=self.entity_namespace,
            parent=self.entity_parent
        )

    def to_representation(self, value):
        if not value:
            return ''
        return six.text_type(value.id())

    def get_attribute(self, instance):
        attr = super(KeyField, self).get_attribute(instance)
        if attr is None:
            return ''
        return attr

    def bind(self, field_name, parent):
        super(KeyField, self).bind(field_name, parent)

        if self.entity_namespace.endswith('()'):
            func = getattr(parent, self.entity_namespace[:-2])
            self.entity_namespace = func()

        if isinstance(self.entity_parent, basestring) and self.entity_parent.endswith('()'):
            func = getattr(parent, self.entity_parent[:-2])
            self.entity_parent = func()


class CharOrMethodField(serializers.CharField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        super(CharOrMethodField, self).__init__(**kwargs)

    def get_attribute(self, instance):
        attr = super(CharOrMethodField, self).get_attribute(instance)
        if attr not in {None, ''}:
            return attr

        if not self.method_name:
            self.method_name = 'get_{field_name}'.format(
                field_name=self.field_name
            )
        attr = getattr(self.parent, self.method_name)(instance)
        return attr
