# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0091_auto_20170908_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='column_four',
            field=wagtail.wagtailcore.fields.StreamField([(b'nav_group', wagtail.wagtailcore.blocks.StructBlock([(b'group_title', wagtail.wagtailcore.blocks.CharBlock(required=False, label=b'Column title')), (b'hide_group_title', wagtail.wagtailcore.blocks.BooleanBlock(required=False, label=b'Hide column title')), (b'status', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'draft-production', b'Draft and production'), (b'production', b'Production'), (b'draft', b'Draft')])), (b'nav_items', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'link', wagtail.wagtailcore.blocks.StructBlock([(b'link_text', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'page_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text=b'Link to a page in Wagtail.', required=False)), (b'external_link', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Enter url for page outside Wagtail.', default=b'#', max_length=1000, required=False))], required=False)), (b'nav_groups', wagtail.wagtailcore.blocks.StreamBlock([(b'nav_group', wagtail.wagtailcore.blocks.StructBlock([(b'nav_items', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'link', wagtail.wagtailcore.blocks.StructBlock([(b'link_text', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'page_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text=b'Link to a page in Wagtail.', required=False)), (b'external_link', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Enter url for page outside Wagtail.', default=b'#', max_length=1000, required=False))], required=False))])))]))]))])))])), (b'featured_content', wagtail.wagtailcore.blocks.StructBlock([(b'status', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'draft-production', b'Draft and production'), (b'production', b'Production'), (b'draft', b'Draft')])), (b'link', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(help_text=b"If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))]))]))], blank=True),
        ),
    ]
