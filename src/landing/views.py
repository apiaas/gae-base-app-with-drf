from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = 'main.html'


main_page = MainPage.as_view()
