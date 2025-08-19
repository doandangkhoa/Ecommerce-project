from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from .models import Cart, CartItem
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
    total_price += tax
    context = {'total_price':total_price, 'quantity':quantity, 'cart_items':cart_items}
    return render(request, 'store/cart.html', context)

def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def add_to_cart(request, product_id):
    price_of_products = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the _cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1,
        )
    cart_item.save()
    price_of_products = cart_item.product.price * cart_item.quantity
    return redirect('cart')
    context = {'cart_item':cart_item, 'price_of_products':price_of_products}
    return render(request, 'store/cart.html', context)