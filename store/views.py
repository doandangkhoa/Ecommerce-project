from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q
from category.models import Category
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
    product_number = products.count()
    context = {'products':products, 'product_number':product_number}
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(Q(category__slug=category_slug) & Q(slug=product_slug))
    except Exception as e:
        raise e
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)