from django.views.generic import TemplateView


class HomeForm(TemplateView):
    template_name = 'index.html'
