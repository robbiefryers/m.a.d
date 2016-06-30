# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0003_auto_20160629_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='photo',
        ),
    ]
