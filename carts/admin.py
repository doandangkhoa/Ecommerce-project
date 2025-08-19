from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'added_date']
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('')
    
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)