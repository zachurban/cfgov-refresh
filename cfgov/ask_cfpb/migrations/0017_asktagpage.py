# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0123_alphabetize_chart_colors'),
        ('ask_cfpb', '0016_modify_help_text_social_sharing_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AskTagPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('ask_category', models.CharField(max_length=255, choices=[('Auto loans', 'Auto loans'), ('Bank accounts and services', 'Bank accounts and services'), ('Credit cards', 'Credit cards'), ('Credit reports and scores', 'Credit reports and scores'), ('Debt collection', 'Debt collection'), ('Families and money', 'Families and money'), ('Money transfers', 'Money transfers'), ('Mortgages', 'Mortgages'), ('Payday loans', 'Payday loans'), ('Prepaid cards', 'Prepaid cards'), ('Student loans', 'Student loans')])),
                ('tag', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
    ]
