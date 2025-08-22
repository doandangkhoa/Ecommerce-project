from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def cart(request,tax=10, total_price=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        count = {}
        for item in cart_items:
            total_price += item.product.price * item.quantity
            quantity += item.quantity
    except CartItem.DoesNotExist:
        pass
    tax = total_price * 0.02
    total = total_price + tax
    context = {'total':total,'total_price':total_price, 'quantity':quantity, 'cart_items':cart_items, 'tax': tax}
    return render(request, 'store/cart.html', context)

def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def add_to_cart(request, product_id):
    # getting product
    product = Product.objects.get(id=product_id)
    
    # getting product variation
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item # name of the variations in the form
            value = request.POST.get(key) # value of the key (color : red)
           
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
        
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    
    # getting a list of items
    cart_items = CartItem.objects.filter(product=product, cart=cart) # list item
    
    # increasing an item quantity 
    if not product_variation:
        if cart_items.exists():
            cart_item = cart_items.first()  # just grab the first one
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')

    # adding item to cart
    cart_item = None
    if cart_items.exists():
        # existing variation --> database
        # current variation --> product_variation
        # item_id --> database
        for item in cart_items:
            existing_variation = list(item.variations.all())
            if set(existing_variation) == set(product_variation):
                cart_item = item
                cart_item.quantity += 1
                cart_item.save()
                break
    if cart_item is None:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity = 1,
            cart = cart,
        )
        # adding variation to product
        cart_item.variations.set(product_variation)
        cart_item.save()    
    return redirect('cart')

def decrement_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    
    cart_item = CartItem.objects.filter(product=product, cart=cart, id=cart_item_id)
    if cart_item:
        cart_item.delete()
        
    return redirect('cart')