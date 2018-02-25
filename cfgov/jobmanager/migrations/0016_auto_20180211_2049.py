# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


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
            ],
        ),
        migrations.AlterField(
            model_name='jobcategory',
            name='blurb',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, blank=True),
        ),
    ]
