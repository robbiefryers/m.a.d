# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0012_auto_20160805_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='number',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
