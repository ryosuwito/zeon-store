from django.contrib import admin
from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin):
    model = Article

class CategoryAdmin(admin.ModelAdmin):
    model = Category

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)