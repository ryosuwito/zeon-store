from django.contrib import admin
from .models import Template, ColorScheme, BrandAsset, BrandIdentity

class TemplateAdmin(admin.ModelAdmin):
    model = Template

class ColorSchemeAdmin(admin.ModelAdmin):
    model = ColorScheme

class BrandAssetAdmin(admin.ModelAdmin):
    model = BrandAsset

class BrandIdentityAdmin(admin.ModelAdmin):
    model = BrandIdentity

admin.site.register(Template, TemplateAdmin)
admin.site.register(ColorScheme, ColorSchemeAdmin)
admin.site.register(BrandAsset, BrandAssetAdmin)
admin.site.register(BrandIdentity, BrandIdentityAdmin)