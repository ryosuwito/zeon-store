# Generated by Django 2.0.8 on 2018-09-27 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0006_auto_20180814_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='activation_code',
            field=models.CharField(blank=True, max_length=8),
        ),
    ]
