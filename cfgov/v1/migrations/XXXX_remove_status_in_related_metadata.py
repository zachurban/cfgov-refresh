# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import migrations, models

from v1.util.migrations import migrate_page_types_and_fields


logger = logging.getLogger(__name__)


def remove_status_in_related_metadata(page_or_revision, data):
    """ Removes "Status" heading and blob from related metadata blocks. """
    # if 'enforcement/actions' not in page_or_revision.url_path:
    #     return data
    content = data['content']
    filtered_content = [
        block for block in content
        if block['type'] == 'text' and  block['value']['heading'] != 'Status'
    ]
    data['content'] = filtered_content
    return data


def forwards(apps, schema_editor):
    page_types_and_fields = [
        ('v1', 'DocumentDetailPage', 'sidefoot', 'related_metadata'),
    ]
    migrate_page_types_and_fields(
        apps,
        page_types_and_fields,
        remove_status_in_related_metadata
    )
    import sys; sys.exit(1)


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0136_remove_htmlblock_from_browsepage'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            migrations.RunPython.noop
        )
    ]
