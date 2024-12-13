from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart
from django.utils.translation import gettext as _

@login_required
def checkout(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        # دریافت اطلاعات فرم
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        
        # ذخیره اطلاعات در پروفایل کاربر
        profile = request.user.profile
        profile.address = address
        profile.postal_code = postal_code
        profile.phone = phone
        profile.save()
        
        # ایجاد سفارش
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            postal_code=postal_code,
            phone=phone,
            total_price=cart.get_total_price()
        )
        
        # ایجاد آیتم‌های سفارش
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                variation=item.get('variation', ''),
                price=item['price'],
                quantity=item['quantity']
            )
            
        # پاک کردن سبد خرید
        cart.clear()
        
        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return redirect('order:order_detail', order.id)
        
    return render(request, 'cart/checkout.html', {
        'cart_items': cart,
        'total_price': cart.get_total_price()
    })
