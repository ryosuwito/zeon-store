# Generated by Django 2.0.8 on 2018-10-11 08:59

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Nama Kategori', max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=('name',), unique=True)),
                ('description', models.TextField(blank=True, help_text='Deskripsi Kategori')),
                ('is_archived', models.BooleanField(default=False, help_text='Centang untuk Menyembunyikan Kategori')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Nama Produk', max_length=200)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=('name',), unique=True)),
                ('description', models.TextField(help_text='Deskripsi Produk')),
                ('photo', models.ImageField(help_text='Foto Produk', upload_to='product_photo')),
                ('photo_alt1', models.ImageField(blank=True, help_text='Foto Produk Alternatif 1', null=True, upload_to='product_photo')),
                ('photo_alt2', models.ImageField(blank=True, help_text='Foto Produk Alternatif 2', null=True, upload_to='product_photo')),
                ('photo_alt3', models.ImageField(blank=True, help_text='Foto Produk Alternatif 3', null=True, upload_to='product_photo')),
                ('photo_alt4', models.ImageField(blank=True, help_text='Foto Produk Alternatif 4', null=True, upload_to='product_photo')),
                ('photo_alt5', models.ImageField(blank=True, help_text='Foto Produk Alternatif 5', null=True, upload_to='product_photo')),
                ('price', models.IntegerField(help_text='Harga Produk', null=True)),
                ('unit_weight', models.IntegerField(help_text='Berat Satuan Produk dalam gram', null=True)),
                ('is_available', models.BooleanField(default=True, help_text='Centang Jika Produk Tersedia')),
                ('is_featured', models.BooleanField(default=False, help_text='Centang untuk menjadikan unggulan')),
                ('is_archived', models.BooleanField(default=False, help_text='Centang untuk Menyembunyikan Produk')),
                ('categories', models.ManyToManyField(help_text='Kategori Produk', related_name='products_in_category', to='st_catalog.Category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]
