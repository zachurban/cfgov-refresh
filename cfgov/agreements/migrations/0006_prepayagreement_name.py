# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0005_add_salesforce_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='prepayagreement',
            name='name',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
