# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0006_auto_20160630_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='act_cat',
            name='endTime',
            field=models.TimeField(default=b'12:00'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='act_cat',
            name='startTime',
            field=models.TimeField(default=b'12:00'),
            preserve_default=True,
        ),
    ]
