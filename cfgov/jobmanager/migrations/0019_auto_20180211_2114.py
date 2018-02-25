# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0018_auto_20180211_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobTypePanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
            ],
            options={
                'ordering': ('job_type',),
            },
        ),
        migrations.RemoveField(
            model_name='joblistingpage',
            name='job_types',
        ),
        migrations.AddField(
            model_name='jobtypepanel',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='job_types', to='jobmanager.JobListingPage'),
        ),
        migrations.AddField(
            model_name='jobtypepanel',
            name='job_type',
            field=models.ForeignKey(related_name='job_type_panels', to='jobmanager.JobType'),
        ),
    ]
