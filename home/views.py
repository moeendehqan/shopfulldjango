from django.views.generic import TemplateView
from .models import Setting

class HomeView(TemplateView):
    template_name = 'home/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.get(pk=1)
        context['description'] = setting.description
        context['keywords'] = setting.keywords
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = setting.title
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        return context


