# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from wagtail.wagtailcore.models import Page, PageRevision

from v1.util.migrations import is_page, migrate_page_types_and_fields


def migrate_email_signup_forwards(page_or_revision, data):

    # Map old gd_code and form_field fields to the new form_fields field
    gd_code = data['gd_code']
    form_field = data['form_field']
    form_fields = []
    for field in form_field:
        form_fields.append({
            'type': 'email',
            'label': field['label'],
            'gd_code': gd_code,
        })
    data['form_fields'] = form_fields

    # Look up privacy links' objects for privacy_act_statement field
    # form_field[0]['info']

    return data


def migrate_email_signup_backwards(page_or_revision, data):
    # raise Exception("Can't migrate email signups backwards")

    # Map new form_fields field to old form_field and gd_code fields
    form_field = []
    form_fields = data['form_fields']
    for field in form_fields:
        # if field['type'] is not 'email':
        #     continue

        form_field.append({
            'type': field['type'],
            'label': field['label'],
            'info': None,
            # These are defaults, since we lost the original values in the
            # forwards migrations
            'btn_text': u'Sign up',
            'is_required': None,
            'placeholder': u'mail@example.com'
        })
        data['gd_code'] = field['gd_code']

    data['form_field'] = form_field
    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'CFGOVPage', 'sidefoot', 'email_signup'),
        # ('v1', 'BlogPage', 'content', 'email_signup'),
        # ('v1', 'LearnPage', 'content', 'email_signup'),
    ]
    migrate_page_types_and_fields(apps, page_types_and_fields,
                                  migrate_email_signup_forwards)


def backwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'CFGOVPage', 'sidefoot', 'govdelivery_signup'),
        # ('v1', 'BlogPage', 'content', 'govdelivery_signup'),
        # ('v1', 'LearnPage', 'content', 'govdelivery_signup'),
    ]
    migrate_page_types_and_fields(apps, page_types_and_fields,
                                  migrate_email_signup_backwards)


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0094_add_govdelivery_signup'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
