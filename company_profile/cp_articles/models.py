from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from django.utils.crypto import get_random_string
from taggit_selectize.managers import TaggableManager
from ckeditor.fields import RichTextField

from membership.models import Member

import datetime

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True, db_index=True, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,related_name='category_site', null=True, blank=True)
    
    def __str__(self):
        return self.title.title()

    def save(self, *args, **kwargs):
        slug = slugify(self.title.lower())
        while Category.objects.filter(slug = slug).exists():
            slug = slugify("%s-%s"%(self.title.lower(),get_random_string(5, allowed_chars='12345677890')))

        self.slug = slug
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

class Article(models.Model):
    class_name = models.CharField(max_length=200, blank=True)
    category = models.ManyToManyField(Category, related_name="article_category", blank=True, null=True)
    slug = models.SlugField(max_length=200,unique=True, db_index=True, blank=True, null=True)
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length=200)
    lead_in = models.CharField(max_length=1000, default="", blank=True)
    content = RichTextField(null=True, blank=True)
    site = models.ForeignKey(Site, related_name="article_site", on_delete=models.CASCADE,null=True, blank=True)
    author = models.ForeignKey(Member, null=True, blank=True,
                                on_delete=models.CASCADE,
                                related_name="article_author", 
                                verbose_name='author')
    owner = models.ForeignKey(Member, null=True, blank=True,
                                on_delete=models.CASCADE, 
                                related_name="article_owner", 
                                verbose_name='owner')
    created_date = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    published_date = models.DateTimeField(db_index=True,null=True, blank=True)
    is_published = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    featured_image = models.ImageField(upload_to = 'cp/user_uploads/featured_images/', null=True, blank=True)

    def __str__(self):
        return self.title.title()


    def save(self, *args, **kwargs):
        slug = slugify(self.title.lower())
        while Article.objects.filter(slug = slug).exists():
            slug = slugify("%s-%s"%(self.title.lower(),get_random_string(5, allowed_chars='12345677890')))

        self.slug = slug
        super(Article, self).save(*args, **kwargs)

    def get_all_tags(self):
        return self.tags.all()

    def get_image_url(self):
        return "%s" % ("/media/%s"%self.featured_image)

    def get_article_url(self):
        return "%s" % (reverse('blog_detail', kwargs={'kategori':self.category.all()[0].slug, 'slug':self.slug}))

    def get_edit_url(self):
        return "%s" % (reverse('cms:article_edit_delete', kwargs={'action':'edit', 'pk':self.pk}))

    def get_delete_url(self):
        return "%s" % (reverse('cms:article_edit_delete', kwargs={'action':'delete', 'pk':self.pk}))
    
    def get_class_name(self):
        return self.class_name

class TempArticle(Article):
    def save(self, *args, **kwargs):
        temps = TempArticle.objects.all().exclude(pk=self.pk)
        if temps:
            for temp in temps:
                temp.delete()
        self.is_published = False
        super(TempArticle, self).save(*args, **kwargs)
    