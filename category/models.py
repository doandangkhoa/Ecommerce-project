from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=255)
    cat_image = models.ImageField(upload_to='photos/categories/', blank=True)
    
    class Meta:
        # name config
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug,])
    # reverse is django utility that lets build urlds by name
    # it finds the urls pattern named 'products_by_category' and 
    # fills in parameters based on what u give in args
    # when u call {{ instance.get_url }} it'll return the full URL to specify that category
    
    def __str__(self):
        return self.name
    
