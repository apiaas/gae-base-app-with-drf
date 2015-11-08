from google.appengine.ext import ndb
from django.http import Http404


class BaseMixin(object):
    """
    Provides additional hooks during initialization and finalization stages.
    """
    def initial(self, request, *args, **kwargs):
        super(BaseMixin, self).initial(request, *args, **kwargs)
        self.initial_hook(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(BaseMixin, self).finalize_response(
            request, response, *args, **kwargs
        )
        self.finalize_hook(request, response, *args, **kwargs)
        return response

    def initial_hook(self, request, *args, **kwargs):
        pass

    def finalize_hook(self, request, response, *args, **kwargs):
        pass

class DataStoreMixin(BaseMixin):
    lookup_field = 'id'

    def set_model_id_type(self, id_string):
        return id_string.isdigit() and int(id_string) or str(id_string)

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        model_key = ndb.Key(
            self.model._get_kind(),
            self.set_model_id_type(self.kwargs[lookup_url_kwarg]),
            parent=queryset.ancestor,
            namespace=queryset.namespace
        )
        obj = queryset.filter(self.model.key == model_key).get()
        if not obj:
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
