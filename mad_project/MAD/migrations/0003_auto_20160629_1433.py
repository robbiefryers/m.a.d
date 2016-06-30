# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAD', '0002_auto_20160629_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='act_cat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('act', models.ForeignKey(to='MAD.Activities', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('photo', models.ImageField(upload_to=b'album_images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='act_cat',
            name='cat',
            field=models.ForeignKey(to='MAD.Categories', null=True),
            preserve_default=True,
        ),
    ]
