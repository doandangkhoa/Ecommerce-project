from django.shortcuts import render, get_object_or_404
from .models import Product
from carts.views import _cart_id
from carts.models import CartItem
from django.db.models import Q
from category.models import Category
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    
    # pagging products    
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    product_number = products.count()
    context = {'page_obj':page_obj, 'product_number':product_number}
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(Q(category__slug=category_slug) & Q(slug=product_slug))
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    except Exception as e:
        raise e
    context = {'product': product, 'in_cart': in_cart}
    return render(request, 'store/product_detail.html', context)

def search_items(request):
    products = Product.objects.none()
    keyword = request.GET.get('keyword')
    
    if keyword:
        products = Product.objects.filter(Q(slug__icontains=keyword) | Q(category__slug__icontains=keyword) |
                                          Q(name__icontains=keyword) | Q(description__icontains=keyword)).order_by('-created_date')
    product_number = products.count()
    context = {'page_obj': products, 'product_number' : product_number}
    return render(request, 'store/store.html', context)