from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(db_index=True,
            max_length = 100,
            help_text="Nama Kategori")
    slug = AutoSlugField(max_length=100, 
            unique=True, 
            db_index=True,
            populate_from=('name',))
    description = models.TextField(blank=True,
            help_text="Deskripsi Kategori")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Kategori") 
    site = models.ForeignKey(Site, on_delete=models.CASCADE,related_name='product_category_site', null=True, blank=True)
   
    class Meta:
        verbose_name_plural = "Categories"

    def get_edit_url(self):
        return "%s" % (reverse('store:category_edit_delete', kwargs={'action':'edit', 'pk':self.pk}))

    def get_delete_url(self):
        return "%s" % (reverse('store:category_edit_delete', kwargs={'action':'delete', 'pk':self.pk}))
   

    def __str__(self):
       return self.name

    def get_url(self):
        return "/store/kategori/%s/" % (self.pk)


class Product(models.Model):
    name = models.CharField(max_length = 200,
            db_index=True,
            help_text="Nama Produk")
    slug = AutoSlugField(max_length=100, 
            db_index=True,
            unique=True, 
            populate_from=('name',))
    description = models.TextField(help_text="Deskripsi Produk")
    photo = models.ImageField(upload_to = 'product_photo',
            help_text="Foto Produk")
    photo_alt1 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 1")
    photo_alt2 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 2")
    photo_alt3 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 3")
    photo_alt4 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 4")
    photo_alt5 = models.ImageField(upload_to = 'product_photo', null=True, blank=True,
            help_text="Foto Produk Alternatif 5")
    price = models.PositiveIntegerField(null=True, help_text="Harga Produk")

    unit_weight = models.PositiveIntegerField(null=True, help_text="Berat Satuan Produk dalam gram")
    is_available = models.BooleanField(default = True,
            help_text="Centang Jika Produk Tersedia")
    is_featured = models.BooleanField(default = False,
            help_text="Centang untuk menjadikan unggulan")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Produk")
    categories = models.ManyToManyField(Category, 
            related_name="products_in_category",
            help_text="Kategori Produk")
    site = models.ForeignKey(Site, on_delete=models.CASCADE,related_name='product_site', null=True, blank=True)
    
    def get_details(self):
        details = {'name': self.name,
                   'weight' : self.unit_weight,
                   'price' : self.price}
        return details

    def get_photo_url(self):
        return "/media/%s" % (self.photo)

    def get_photo_alt1_url(self):
        return "/media/%s" % (self.photo_alt1)
    def get_photo_alt2_url(self):
        return "/media/%s" % (self.photo_alt2)
    def get_photo_alt3_url(self):
        return "/media/%s" % (self.photo_alt3)
    def get_photo_alt4_url(self):
        return "/media/%s" % (self.photo_alt4)
    def get_photo_alt5_url(self):
        return "/media/%s" % (self.photo_alt5)

    def get_edit_url(self):
        return "%s" % (reverse('store:product_edit_delete', kwargs={'action':'edit', 'pk':self.pk}))

    def get_delete_url(self):
        return "%s" % (reverse('store:product_edit_delete', kwargs={'action':'delete', 'pk':self.pk}))
    
    def get_detail_url(self):
        return reverse('storefront:product_detail', kwargs={'product_pk':self.pk})

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
       return self.name