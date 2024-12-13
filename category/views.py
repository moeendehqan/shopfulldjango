from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Category
from home.models import Setting
from product.models import Product

# Create your views here.
class CategoryView(TemplateView):
    template_name = 'category/category.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=kwargs['slug'])
        setting = Setting.objects.get(pk=1)
        
        products = Product.objects.filter(
            category=category,
            published=True
        ).prefetch_related('variation_set')
        
        context['category'] = category
        context['products'] = products
        context['description'] = category.description
        context['keywords'] = category.keywords
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = setting.title + ' | ' + category.name
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        return context

class AllCategoriesView(ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.get(pk=1)
        context['description'] = 'تمام دسته‌بندی‌های فروشگاه'
        context['keywords'] = 'دسته‌بندی‌ها، فروشگاه'
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = setting.title + ' | دسته‌بندی‌ها'
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        return context

