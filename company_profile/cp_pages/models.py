from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.dispatch import receiver

from taggit_selectize.managers import TaggableManager
from ckeditor.fields import RichTextField

from membership.models import Member

import datetime
import random
import string

class PageModel(models.Model):
    class_name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextField(null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True)
    site = models.ForeignKey(Site, related_name="site_page", on_delete=models.CASCADE,null=True, blank=True)
    owner = models.ForeignKey(Member, null=True, blank=True,
                                on_delete=models.CASCADE, 
                                related_name="page_owner", 
                                verbose_name='owner')
    created_date = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    is_published = models.BooleanField(default=False, db_index=True)
    is_preview = models.BooleanField(default=False, db_index=True)
    banner_image_1 = models.ImageField(upload_to = 'cp/user_uploads/banner_images/', null=True, blank=True)
    banner_image_2 = models.ImageField(upload_to = 'cp/user_uploads/banner_images/', null=True, blank=True)
    banner_image_3 = models.ImageField(upload_to = 'cp/user_uploads/banner_images/', null=True, blank=True)
    meta_description = models.CharField(max_length=1000, default="", blank=True)
    meta_keyword = TaggableManager(blank=True)
    page_view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title.title()
    
    def get_banner_image_1_url(self):
        return ("/media/%s"%self.banner_image_1)
    
    def get_banner_image_2_url(self):
        return ("/media/%s"%self.banner_image_2)
    
    def get_banner_image_3_url(self):
        return ("/media/%s"%self.banner_image_3)

    def get_page_url(self):
        return "/%s/" % (self.slug)

    def get_edit_url(self):
        return "%s" % (reverse('cms:page_edit_delete', kwargs={'action':'edit', 'pk':self.pk}))

    def get_delete_url(self):
        return "%s" % (reverse('cms:page_edit_delete', kwargs={'action':'delete', 'pk':self.pk}))
    
    def get_class_name(self):
        return self.class_name

class TempPageModel(PageModel):
    def save(self, *args, **kwargs):
        temps = TempPageModel.objects.all().exclude(pk=self.pk)
        if temps:
            for temp in temps:
                temp.delete()
        self.slug = slugify(self.title.lower() + ''.join(random.choices(string.ascii_lowercase + string.digits, k=11)))
        self.is_published = False
        self.is_preview = True
        super(TempPageModel, self).save(*args, **kwargs) 


@receiver(post_save, sender=PageModel)
def create_page(sender, instance, created, **kwargs):
    if created:
        slug = slugify(instance.title.lower())
        while PageModel.objects.filter(slug = slug).exists():
            slug = slugify("%s-%s"%(instance.title.lower(),get_random_string(5, allowed_chars='12345677890')))

        instance.slug = slug
        instance.save()