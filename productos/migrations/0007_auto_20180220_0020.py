# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_auto_20180220_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='offer_day_to',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
