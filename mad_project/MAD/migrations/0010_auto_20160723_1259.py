# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0009_auto_20160721_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='contactEmail',
            field=models.EmailField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activities',
            name='contactName',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activities',
            name='number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activities',
            name='special',
            field=models.CharField(max_length=256, blank=True),
        ),
    ]
