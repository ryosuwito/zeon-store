from django.contrib import admin
from .models import Member, PackageGroup

class PackageGroupAdmin(admin.ModelAdmin):
    model = PackageGroup

class MemberAdmin(admin.ModelAdmin):
    model = Member
    exclude = ['slug']

admin.site.register(PackageGroup, PackageGroupAdmin)
admin.site.register(Member, MemberAdmin)