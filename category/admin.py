from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} # automatically fill in the slug field based on the name field
    list_display = ('name', 'slug')
    
admin.site.register(Category, CategoryAdmin)