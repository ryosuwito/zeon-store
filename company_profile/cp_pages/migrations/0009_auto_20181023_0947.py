# Generated by Django 2.0.8 on 2018-10-23 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp_pages', '0008_auto_20181002_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagemodel',
            name='page_view',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
