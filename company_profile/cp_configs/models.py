from django.db import models

class Template(models.Model):
    name = models.CharField(max_length=150, blank=True)
    dir_name = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = "Templates"

class ColorScheme(models.Model):
    name = models.CharField(max_length=150, blank=True)
    primary_color = models.CharField(max_length=6, blank=True)
    dark_color = models.CharField(max_length=6, blank=True)
    accent_color = models.CharField(max_length=6, blank=True)
    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = "Color Schemes"

class BrandAsset(models.Model):
    favicon = models.ImageField(upload_to = 'cp/favicon', blank=True, null=True)
    hero_image_1 = models.ImageField(upload_to = 'cp/hero_image', blank=True, null=True)
    hero_image_2 = models.ImageField(upload_to = 'cp/hero_image', blank=True, null=True)
    hero_image_3 = models.ImageField(upload_to = 'cp/hero_image', blank=True, null=True)
    brand_logo = models.ImageField(upload_to = 'cp/brand_logo', blank=True, null=True)
    main_photo_1 = models.ImageField(upload_to = 'cp/main_photo_1', blank=True, null=True)
    main_photo_2 = models.ImageField(upload_to = 'cp/main_photo_2', blank=True, null=True)
    extra_image_1 = models.ImageField(upload_to = 'cp/extra_image', blank=True, null=True)
    extra_image_2 = models.ImageField(upload_to = 'cp/extra_image', blank=True, null=True)
    extra_image_3 = models.ImageField(upload_to = 'cp/extra_image', blank=True, null=True)
    class Meta:
        verbose_name_plural = "Brand Assets"

    def get_extra_image_1_url(self):
        return ("/media/%s"%self.extra_image_1)
    def get_extra_image_2_url(self):
        return ("/media/%s"%self.extra_image_2)
    def get_extra_image_3_url(self):
        return ("/media/%s"%self.extra_image_3)
    def get_main_photo_1_url(self):
        return ("/media/%s"%self.main_photo_1)
    def get_main_photo_2_url(self):
        return ("/media/%s"%self.main_photo_2)
    def get_hero_image_1_url(self):
        return ("/media/%s"%self.hero_image_1)
    def get_hero_image_2_url(self):
        return ("/media/%s"%self.hero_image_2)
    def get_hero_image_3_url(self):
        return ("/media/%s"%self.hero_image_3)
    def get_favicon(self):
        return ("/media/%s"%self.favicon)
    def get_brand_logo_url(self):
        return ("/media/%s"%self.brand_logo)
        
class BrandIdentity(models.Model):
    company_name = models.CharField(max_length=250, blank=True)
    company_tagline = models.CharField(max_length=350, blank=True)
    company_address = models.CharField(max_length=450, blank=True)
    company_email_address = models.EmailField(blank=True, null=True)
    company_phone_number = models.CharField(max_length=35, blank=True)
    company_fax_number = models.CharField(max_length=35, blank=True)
    company_facebook = models.CharField(max_length=150, blank=True)
    company_instagram = models.CharField(max_length=150, blank=True)
    company_whatsapp = models.CharField(max_length=35, blank=True)
    class Meta:
        verbose_name_plural = "Brand Identities"
