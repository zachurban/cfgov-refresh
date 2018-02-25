# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0017_joblistingpage_manytomany'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joblistingpage',
            name='manytomany',
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='job_types',
            field=modelcluster.fields.ParentalManyToManyField(related_name='job_listing_pages', to='jobmanager.JobType', blank=True),
        ),
    ]
