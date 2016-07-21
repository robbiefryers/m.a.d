# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0008_auto_20160630_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act_cat',
            name='act',
            field=models.ForeignKey(related_name=b'cats', to='MAD.Activities', null=True),
        ),
        migrations.AlterField(
            model_name='act_day',
            name='act',
            field=models.ForeignKey(related_name=b'days', to='MAD.Activities', null=True),
        ),
    ]
