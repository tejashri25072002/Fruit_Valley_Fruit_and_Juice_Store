from django.contrib import admin
from fruitapp.models import fruit_product,juice_product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','is_active']
    list_filter=['cat','price','is_active']

class ProductAdmin1(admin.ModelAdmin):
    list_display=['id','name','price','juicecat','is_active']
    list_filter=['juicecat','price','is_active']

admin.site.register(fruit_product,ProductAdmin)
admin.site.register(juice_product,ProductAdmin1)