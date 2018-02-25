# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0016_auto_20180211_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblistingpage',
            name='manytomany',
            field=modelcluster.fields.ParentalManyToManyField(to='jobmanager.JobType', blank=True),
        ),
    ]
