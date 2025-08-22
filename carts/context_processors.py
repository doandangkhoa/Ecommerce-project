from .models import Cart, CartItem
from .views import _cart_id
def counter(request):
    count_items = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.all().filter(cart=cart[:1]) # taking the fist element
            for item in cart_items:
                count_items += item.quantity
        except Cart.DoesNotExist:
            count_items = 0
    return {"number_items" : count_items}