from django.views.generic import TemplateView
from .models import Setting, Slider
import random
from product.models import Product, Variation
from django.db.models import Avg, Count, F, ExpressionWrapper, DecimalField, Subquery, OuterRef

class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.first()
        sliders = Slider.objects.all()
        
        # انتخاب تصادفی یک اسلایدر
        random_slider = random.choice(sliders) if sliders else None
        
        # محصولات با بیشترین تخفیف (یک تنوع با بیشترین تخفیف برای هر محصول)
        max_discount_subquery = Variation.objects.filter(
            product=OuterRef('product')
        ).annotate(
            discount_percentage=ExpressionWrapper(
                (F('price') - F('price_after_discount')) * 100.0 / F('price'),
                output_field=DecimalField()
            )
        ).order_by('-discount_percentage')
        
        discounted_variations = Variation.objects.annotate(
            discount_percentage=ExpressionWrapper(
                (F('price') - F('price_after_discount')) * 100.0 / F('price'),
                output_field=DecimalField()
            )
        ).filter(
            price_after_discount__lt=F('price'),
            pk=Subquery(max_discount_subquery.values('pk')[:1])
        ).order_by('-discount_percentage')[:5]
        
        # محصولات با بیشترین امتیاز کاربر
        top_rated_products_with_variations = Product.objects.annotate(
            avg_rating=Avg('review__rate'),
            max_discount_percentage=Subquery(
                Variation.objects.filter(product=OuterRef('pk'))
                .annotate(
                    discount_percentage=ExpressionWrapper(
                        (F('price') - F('price_after_discount')) * 100.0 / F('price'),
                        output_field=DecimalField()
                    )
                )
                .order_by('-discount_percentage')
                .values('discount_percentage')[:1]
            )
        ).order_by('-avg_rating')[:5]
        
        # محصولات پرفروش
        best_selling_products_with_variations = Product.objects.annotate(
            max_discount_percentage=Subquery(
                Variation.objects.filter(product=OuterRef('pk'))
                .annotate(
                    discount_percentage=ExpressionWrapper(
                        (F('price') - F('price_after_discount')) * 100.0 / F('price'),
                        output_field=DecimalField()
                    )
                )
                .order_by('-discount_percentage')
                .values('discount_percentage')[:1]
            )
        ).order_by('-count_sell')[:5]
        
        # محصولات جدید
        newest_products_with_variations = Product.objects.annotate(
            max_discount_percentage=Subquery(
                Variation.objects.filter(product=OuterRef('pk'))
                .annotate(
                    discount_percentage=ExpressionWrapper(
                        (F('price') - F('price_after_discount')) * 100.0 / F('price'),
                        output_field=DecimalField()
                    )
                )
                .order_by('-discount_percentage')
                .values('discount_percentage')[:1]
            )
        ).order_by('-created_at')[:5]
        
        # اضافه کردن اولین تنوع برای هر محصول
        def add_first_variation(products):
            products_with_variations = []
            for product in products:
                first_variation = product.variation_set.first()
                if first_variation:
                    first_variation.product = product
                    first_variation.max_discount_percentage = product.max_discount_percentage
                    if hasattr(product, 'avg_rating'):
                        first_variation.avg_rating = product.avg_rating
                    products_with_variations.append(first_variation)
            return products_with_variations
        
        context['description'] = setting.description
        context['keywords'] = setting.keywords
        context['author'] = setting.author
        context['robots'] = 'index, follow'
        context['title'] = setting.title
        context['logo'] = setting.logo
        context['favicon'] = setting.favicon
        context['random_slider'] = random_slider
        context['setting'] = setting
        
        # اضافه کردن محصولات به context
        context['discounted_products'] = discounted_variations
        context['top_rated_products'] = add_first_variation(top_rated_products_with_variations)
        context['best_selling_products'] = add_first_variation(best_selling_products_with_variations)
        context['newest_products'] = add_first_variation(newest_products_with_variations)
        
        # چاپ اطلاعات محصولات
        for category, products in [
            ('محصولات با بیشترین تخفیف', context['discounted_products']),
            ('محصولات با بیشترین امتیاز', context['top_rated_products']),
            ('محصولات پرفروش', context['best_selling_products']),
            ('محصولات جدید', context['newest_products'])
        ]:
            print(f"\n{category}:")
            for product in products:
                print(f"ID: {product.product.id}, Name: {product.product.name}, Slug: {product.product.slug}")
        
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



