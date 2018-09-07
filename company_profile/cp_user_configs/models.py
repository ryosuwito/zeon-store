from django.db import models
from membership.models import Member
from company_profile.cp_configs.models import Template, ColorScheme, BrandAsset, BrandIdentity

class UserConfigs(models.Model):
    member = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True, blank=True)
    templates = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    color_scheme = models.ForeignKey(ColorScheme, on_delete=models.SET_NULL, null=True, blank=True)
    brand_assets = models.ForeignKey(BrandAsset, on_delete=models.SET_NULL, null=True, blank=True)
    brand_identity = models.ForeignKey(BrandIdentity, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.member.user.username.title()

    class Meta:
        verbose_name_plural = "User Configs"