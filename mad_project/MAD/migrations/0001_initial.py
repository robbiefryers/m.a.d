# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('venue', models.CharField(max_length=128)),
                ('postcode', models.CharField(max_length=16)),
                ('agesLower', models.IntegerField(default=3)),
                ('agesUpper', models.IntegerField(default=100)),
                ('contact', models.CharField(max_length=256)),
                ('special', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
