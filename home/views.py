from django.views.generic import TemplateView
from .models import Setting, Slider
import random

class HomeView(TemplateView):
    template_name = 'home/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.first()
        sliders = Slider.objects.all()
        
        # انتخاب تصادفی یک اسلایدر
        random_slider = random.choice(sliders) if sliders else None
        
        context['description'] = setting.description
        context['keywords'] = setting.keywords
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = setting.title
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        context['random_slider'] = random_slider
        context['setting'] = setting
        return context



