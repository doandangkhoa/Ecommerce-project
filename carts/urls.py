from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('decrement_item/<int:product_id>/<int:cart_item_id>/', views.decrement_item, name='decrement-item'),
    path('remove_item/<int:product_id>/<int:cart_item_id>/', views.remove_item, name='remove-item')
]