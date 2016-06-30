# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0005_activities_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activities',
            name='contact',
        ),
        migrations.AddField(
            model_name='activities',
            name='contactEmail',
            field=models.EmailField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activities',
            name='contactName',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activities',
            name='number',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
