# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0015_job_page_field_updates'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Job type')),
                ('govdelivery_question_id', models.CharField(max_length=255)),
                ('govdelivery_answer_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='JobTypePanel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('job_listing', modelcluster.fields.ParentalKey(related_name='job_types', to='jobmanager.JobListingPage')),
                ('job_type', models.ForeignKey(related_name='job_type_panels', to='jobmanager.JobType')),
            ],
            options={
                'ordering': ('job_type',),
            },
        ),
        migrations.AddField(
            model_name='grade',
            name='govdelivery_answer_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grade',
            name='govdelivery_question_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobcategory',
            name='blurb',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, blank=True),
        ),
    ]
