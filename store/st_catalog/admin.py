from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    exclude = ['slug']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    exclude = ['slug']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)