# Generated by Django 2.0.8 on 2018-10-18 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0009_auto_20181011_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='subcription',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Company Profile'), (1, 'Online Shop')], default=0),
        ),
    ]
