from django.views.generic import DetailView, ListView
from .models import Product
from home.models import Setting
from django.core import serializers
import json

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.get(pk=1)
        product = self.get_object()
        variations = product.variation_set.filter(published=True)
        
        # دریافت variation_id از کوئری پارامتر
        selected_variation_id = self.request.GET.get('variation')
        selected_variation = None
        
        if selected_variation_id:
            try:
                selected_variation = variations.get(id=selected_variation_id)
            except:
                selected_variation = variations.first()
        else:
            selected_variation = variations.first()
            
        context['variations'] = variations
        context['selected_variation'] = selected_variation
        
        # SEO و اطلاعات پایه
        context['description'] = product.description
        context['keywords'] = product.keywords
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = setting.title + ' | ' + product.name
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        
        # تبدیل variations به JSON برای استفاده در JavaScript
        variations_data = []
        for var in variations:
            # تهیه لیست تصاویر برای هر تنوع
            images = [{'url': img.image.url, 'alt': img.alt} for img in var.image.all()]
            
            variations_data.append({
                'id': var.id,
                'price': var.price,
                'price_after_discount': var.price_after_discount,
                'stock': var.stock,
                'color': var.color.name if var.color else None,
                'size': var.size.name if var.size else None,
                'images': images,
                'default_image': product.image.url,  # تصویر پیش‌فرض محصول
            })
        
        context['variations_json'] = json.dumps(variations_data)
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'


