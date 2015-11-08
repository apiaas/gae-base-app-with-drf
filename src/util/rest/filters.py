from django.utils import six
from google.appengine.ext import ndb
from rest_framework import filters, serializers
from rest_framework.serializers import IntegerField, CharField
from util.rest.fields import KeyField


class FieldFilter(filters.BaseFilterBackend):
    """
    Takes a list of object fields with search values from url query and
    constructs ndb query set with objects that match those values.

    ?field1=A&field2=B will match objects that have A and B values.
    """

    def sanitize(self, field, value, kwargs):

        if value in {'null', 'None', 'none'}:
            return field, None

        namespace = kwargs.get('location') and kwargs['location'].namespace or ''

        def validate_key_field(f, v):
            if isinstance(v, unicode):
                id_type = unicode
            else:
                id_type = str

            if id_type(v).isdigit():
                field_value = int(v)
                id_type = int

            return KeyField(
                entity_name=f._kind, entity_namespace=namespace,
                id_type=id_type
            ).to_internal_value(field_value)

        ndb2rest = {
            ndb.IntegerProperty: lambda _, v: IntegerField().to_internal_value(v),
            ndb.StringProperty: lambda _, v: CharField(
                max_length=500, min_length=1
            ).to_internal_value(v),
            ndb.KeyProperty: validate_key_field
        }

        clean = ndb2rest.get(field.__class__)
        if not clean:
            msg = 'This type of filter is not supported yet.'
            raise serializers.ValidationError(msg)

        return field, clean(field, value)

    def filter_queryset(self, request, queryset, view):
        search_fields = []
        for key, value in request.query_params.items():
            # Guido recommends using ._properties here instead of getattr
            field = view.ndb_class._properties.get(key)
            if field and value:
                search_fields.append(self.sanitize(field, value, view.kwargs))

        if not search_fields:
            return queryset

        terms = ndb.AND(*(field == value for field, value in search_fields))
        return queryset.filter(terms)


class OrderingFilter(filters.BaseFilterBackend):
    ordering_fields = []
    ordering_param = None

    def get_ordering(self, request):
        params = request.query_params.get(self.ordering_param)
        if params:
            return [param.strip() for param in params.split(',')]

    def get_default_ordering(self, view):
        ordering = getattr(view, 'ordering', None)
        if isinstance(ordering, six.string_types):
            return (ordering,)
        return ordering

    def remove_invalid_fields(self, ordering, view):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        return [term for term in ordering if term.lstrip('-') in valid_fields]

    def build_ordering_param(self, path, root):
        param = root
        for part in path:
            param = getattr(param, part.lstrip('-'))

        if path[0].startswith('-'):
            return -param

        return param

    def filter_queryset(self, request, queryset, view):
        self.ordering_param = getattr(view, 'ordering_param', None)
        ordering = self.get_ordering(request)

        if ordering:
            # Skip any incorrect parameters
            ordering = self.remove_invalid_fields(ordering, view)

        if not ordering:
            # Use 'ordering' attribute by default
            ordering = self.get_default_ordering(view)

        if ordering:
            sort_params = [self.build_ordering_param(path, view.ndb_class)
                           for path in [order.split('.') for order in ordering]]

            return queryset.order(*sort_params)

        return queryset
