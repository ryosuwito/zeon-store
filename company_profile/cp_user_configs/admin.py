from django.contrib import admin
from .models import UserConfigs

class UserConfigsAdmin(admin.ModelAdmin):
    model = UserConfigs

admin.site.register(UserConfigs, UserConfigsAdmin)

