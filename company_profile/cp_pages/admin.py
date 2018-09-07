from django.contrib import admin
from .models import PageModel

class PageAdmin(admin.ModelAdmin):
    model = PageModel

admin.site.register(PageModel, PageAdmin)

