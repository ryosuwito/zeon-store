# Generated by Django 2.0.8 on 2018-10-23 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('st_purchase_order', '0003_auto_20181023_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseorder',
            options={'ordering': ['-created_date'], 'verbose_name': 'PurchaseOrder', 'verbose_name_plural': 'Purchase Orders'},
        ),
    ]
