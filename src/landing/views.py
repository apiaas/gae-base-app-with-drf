from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = 'landing/main.html'

    # later we'll move this to the base class, it's ok for now
    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['page_title'] = u'APIAAS | Api as a service'
        context['page_header'] = u'Welcome'
        context['page_header_desc'] = u'Base GAE project with Django Rest Framework'
        
        return context


main_page = MainPage.as_view()
