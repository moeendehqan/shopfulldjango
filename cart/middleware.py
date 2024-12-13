from .models import Cart

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.get('cart_id'):
                cart = Cart.objects.create(user=None)
                request.session['cart_id'] = str(cart.id)
            else:
                try:
                    cart = Cart.objects.get(id=request.session['cart_id'])
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(user=None)
                    request.session['cart_id'] = str(cart.id)
                except ValueError:
                    cart = Cart.objects.create(user=None)
                    request.session['cart_id'] = str(cart.id)

        request.cart = cart
        response = self.get_response(request)
        return response