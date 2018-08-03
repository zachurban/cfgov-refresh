# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0016_modify_help_text_social_sharing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='snippet',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Optional answer intro, 180-200 characters max.', blank=True),
        ),
    ]
