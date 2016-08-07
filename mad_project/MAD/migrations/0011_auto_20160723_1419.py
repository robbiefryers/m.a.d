# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0010_auto_20160723_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='owner',
            field=models.ForeignKey(related_name=b'acs', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
