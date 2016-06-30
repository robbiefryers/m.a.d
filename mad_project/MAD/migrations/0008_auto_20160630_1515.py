# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0007_auto_20160630_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='act_day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=32)),
                ('startTime', models.TimeField(default=b'12:00')),
                ('endTime', models.TimeField(default=b'12:00')),
                ('act', models.ForeignKey(to='MAD.Activities', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='act_cat',
            name='endTime',
        ),
        migrations.RemoveField(
            model_name='act_cat',
            name='startTime',
        ),
    ]
