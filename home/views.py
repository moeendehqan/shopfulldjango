from django.views.generic import TemplateView
from .models import Setting, Slider
import random
from django.shortcuts import render
from product.models import Product
from django.db.models import Avg, Count, F

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

class AboutUsView(TemplateView):
    template_name = 'home/aboutus.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.first()
        
        context['description'] = setting.description
        context['keywords'] = setting.keywords
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = 'درباره ما - ' + setting.title
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        context['setting'] = setting
        
        return context

def home_view(request):
    # محصولات با بیشترین تخفیف
    discounted_products = Product.objects.order_by('-discount_percentage')[:5]
    
    # محصولات با بیشترین امتیاز کاربر
    top_rated_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]
    
    # محصولات پرفروش
    best_selling_products = Product.objects.annotate(
        total_sales=Count('orderitem')
    ).order_by('-total_sales')[:5]
    
    # محصولات جدید
    newest_products = Product.objects.order_by('-created_at')[:5]
    
    context = {
        'discounted_products': discounted_products,
        'top_rated_products': top_rated_products,
        'best_selling_products': best_selling_products,
        'newest_products': newest_products,
    }
    
    return render(request, 'home/home.html', context)



