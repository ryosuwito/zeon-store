from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from taggit_selectize.managers import TaggableManager
from ckeditor.fields import RichTextField

from membership.models import Member

import datetime

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,related_name='category_site', null=True, blank=True)
    
    def __str__(self):
        return self.title.title()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title.lower())
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

class Article(models.Model):
    category = models.ManyToManyField(Category, related_name="article_category", blank=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True)
    tags = TaggableManager()
    title = models.CharField(max_length=200)
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
        self.slug = slugify(self.title.lower())
        super(Article, self).save(*args, **kwargs)
        if not self.category.all() :
            self.category.add(Category.objects.get_or_create(site=self.site, title="post")[0])
        super(Article, self).save(*args, **kwargs)

    def get_all_tags(self):
        return self.tags.all()

    def get_article_url(self):
        return "%s" % (reverse('blog_detail', kwargs={'kategori':self.category.all()[0].slug, 'slug':self.slug}))

    def get_edit_url(self):
        return "%s" % (reverse('cms:article_edit_delete', kwargs={'action':'edit', 'pk':self.pk}))

    def get_delete_url(self):
        return "%s" % (reverse('cms:article_edit_delete', kwargs={'action':'delete', 'pk':self.pk}))
