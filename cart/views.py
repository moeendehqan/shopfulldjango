from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from product.models import Product, Variation
from home.models import Setting

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart

@require_POST
def add_to_cart(request):
    try:
        variation_id = request.POST.get('variation_id')
        quantity = int(request.POST.get('quantity', 1))
        
        variation = Variation.objects.get(id=variation_id)
        if variation.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': 'موجودی کافی نیست'
            }, status=400)

        cart = get_or_create_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            variation=variation,
            defaults={
                'product': variation.product,
                'quantity': quantity
            }
        )
        
        if not created:
            if variation.stock < (cart_item.quantity + quantity):
                return JsonResponse({
                    'success': False,
                    'message': 'موجودی کافی نیست'
                }, status=400)
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({
            'success': True,
            'message': 'محصول با موفقیت به سبد خرید اضافه شد',
            'cart_items_count': cart.items.count(),
            'variation_name': str(variation),
            'product_name': variation.product.name
        })

    except Variation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'تنوع محصول یافت نشد'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'خطا در افزودن به سبد خرید'
        }, status=400)

def view_cart(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'variation').all()
    setting = Setting.objects.get(pk=1)

    
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'title': 'سبد خرید',
        'description': 'مشاهده سبد خرید و محصولات',
        'author': setting.author,
        'robots': 'index, follow',
        'logo': setting.logo,
        'favicon': setting.favicon,
        'title': setting.title + ' | ' + 'سبد خرید',

    }
    
    return render(request, 'cart/cart.html', context)

# Create your views here.
