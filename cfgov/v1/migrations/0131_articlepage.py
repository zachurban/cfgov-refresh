# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-27 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import v1.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('v1', '0130_add_related_posts_view_more_override'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('tag', models.CharField(blank=True, max_length=500)),
                ('category', models.CharField(blank=True, max_length=500)),
                ('limit', models.CharField(default=b'3', help_text=b'Limit list to this number of items', max_length=3)),
                ('header', wagtail.wagtailcore.fields.StreamField([(b'hero', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Maximum character count: 25 (including spaces)', required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(help_text=b'Maximum character count: 185 (including spaces)', required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), help_text=b'If your hero needs a call-to-action link, enter it here, rather than inside the body field.')), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Select to render any links given above as buttons.', required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(help_text=b'Should be exactly 390px tall, and up to 940px wide, unless this is an overlay or bleeding style hero.', required=False)), (b'is_overlay', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Select if you want the provided image to be a background image under the entire hero.', required=False)), (b'background_color', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Specify a hex value (with the # sign) from our official palette: https://github.com/cfpb/cf-theme-cfpb/blob/master/src/color-palette.less', required=False)), (b'is_white_text', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Turns the hero text white. Useful if using a dark background color or background image.', required=False)), (b'cta_link_color', wagtail.wagtailcore.blocks.CharBlock(help_text=b'If using a dark background color or background image, you may need to specify an alternate color for the call-to-action link. Specify a hex value (with the # sign) from our official palette: https://github.com/cfpb/cf-theme-cfpb/blob/master/src/color-palette.less', label=b'CTA link color', required=False)), (b'is_bleeding', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Select if you want the provided image to bleed vertically off the top and bottom of the hero.', required=False)), (b'small_image', wagtail.wagtailimages.blocks.ImageChooserBlock(help_text=b'Provide an alternate image for small displays when using a bleeding or overlay hero.', required=False))])), (b'text_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'eyebrow', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Optional: Adds an H5 eyebrow above H1 heading text. Only use in conjunction with heading.', label=b'Pre-heading', required=False)), (b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Check this to add a horizontal rule line to bottom of text introduction.', label=b'Has bottom rule', required=False))]))], blank=True)),
                ('content', wagtail.wagtailcore.fields.StreamField([(b'info_unit_group', wagtail.wagtailcore.blocks.StructBlock([(b'format', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'50-50', b'50/50'), (b'33-33-33', b'33/33/33'), (b'25-75', b'25/75')], help_text=b'Choose the number and width of info unit columns.', label=b'Format')), (b'heading', wagtail.wagtailcore.blocks.StructBlock([(b'text', v1.blocks.HeadingTextBlock(required=False)), (b'level', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'h2', b'H2'), (b'h3', b'H3'), (b'h4', b'H4')])), (b'icon', v1.blocks.HeadingIconBlock(help_text=b'Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#icons">See full list of icons</a>', required=False))], required=False)), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(help_text=b'If this field is not empty, the Heading field must also be set.', required=False)), (b'link_image_and_heading', wagtail.wagtailcore.blocks.BooleanBlock(default=True, help_text=b"Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", required=False)), (b'has_top_rule_line', wagtail.wagtailcore.blocks.BooleanBlock(default=False, help_text=b'Check this to add a horizontal rule line to top of info unit group.', required=False)), (b'lines_between_items', wagtail.wagtailcore.blocks.BooleanBlock(default=False, help_text=b'Check this to show horizontal rule lines between info units.', label=b'Show rule lines between items', required=False)), (b'info_units', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(help_text=b"If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))])), (b'heading', wagtail.wagtailcore.blocks.StructBlock([(b'text', v1.blocks.HeadingTextBlock(required=False)), (b'level', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'h2', b'H2'), (b'h3', b'H3'), (b'h4', b'H4')])), (b'icon', v1.blocks.HeadingIconBlock(help_text=b'Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#icons">See full list of icons</a>', required=False))], default={b'level': b'h3'}, required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True, required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))]))), (b'sharing', wagtail.wagtailcore.blocks.StructBlock([(b'shareable', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'If checked, share links will be included below the items.', label=b'Include sharing links?', required=False)), (b'share_blurb', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Sets the tweet text, email subject line, and LinkedIn post text.', required=False))]))])), (b'well', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(label=b'Well', required=False))])), (b'feedback', wagtail.wagtailcore.blocks.StructBlock([(b'was_it_helpful_text', wagtail.wagtailcore.blocks.CharBlock(default=b'Was this page helpful to you?', help_text=b'Use this field only for feedback forms that use "Was this helpful?" radio buttons.', required=False)), (b'intro_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Optional feedback intro', required=False)), (b'question_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Optional expansion on intro', required=False)), (b'radio_intro', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Leave blank unless you are building a feedback form with extra radio-button prompts, as in /owning-a-home/help-us-improve/.', required=False)), (b'radio_text', wagtail.wagtailcore.blocks.CharBlock(default=b'This information helps us understand your question better.', required=False)), (b'radio_question_1', wagtail.wagtailcore.blocks.CharBlock(default=b'How soon do you expect to buy a home?', required=False)), (b'radio_question_2', wagtail.wagtailcore.blocks.CharBlock(default=b'Do you currently own a home?', required=False)), (b'button_text', wagtail.wagtailcore.blocks.CharBlock(default=b'Submit')), (b'contact_advisory', wagtail.wagtailcore.blocks.RichTextBlock(help_text=b'Use only for feedback forms that ask for a contact email', required=False))])), (b'image_text_25_75_group', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title', required=False)), (b'link_image_and_heading', wagtail.wagtailcore.blocks.BooleanBlock(default=False, help_text=b"Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", required=False)), (b'image_texts', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(help_text=b"If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))])), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])))])), (b'image_text_50_50_group', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title', required=False)), (b'link_image_and_heading', wagtail.wagtailcore.blocks.BooleanBlock(default=False, help_text=b"Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", required=False)), (b'sharing', wagtail.wagtailcore.blocks.StructBlock([(b'shareable', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'If checked, share links will be included below the items.', label=b'Include sharing links?', required=False)), (b'share_blurb', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Sets the tweet text, email subject line, and LinkedIn post text.', required=False))])), (b'image_texts', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True, required=False)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(help_text=b"If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))])), (b'is_widescreen', wagtail.wagtailcore.blocks.BooleanBlock(label=b'Use 16:9 image', required=False)), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(label=b'Show links as button', required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))])))])), (b'half_width_link_blob_group', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title', required=False)), (b'has_top_border', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'has_bottom_border', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'link_blobs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(label=b'H3 heading', required=False)), (b'sub_heading', wagtail.wagtailcore.blocks.CharBlock(label=b'H4 heading', required=False)), (b'sub_heading_icon', wagtail.wagtailcore.blocks.CharBlock(help_text=b'A list of icon names can be obtained at: https://cfpb.github.io/capital-framework/components/cf-icons/. Examples: linkedin-square, facebook-square, etc.', label=b'H4 heading icon', required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True, required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))])))])), (b'third_width_link_blob_group', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title', required=False)), (b'has_top_border', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'has_bottom_border', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'link_blobs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(label=b'H3 heading', required=False)), (b'sub_heading', wagtail.wagtailcore.blocks.CharBlock(label=b'H4 heading', required=False)), (b'sub_heading_icon', wagtail.wagtailcore.blocks.CharBlock(help_text=b'A list of icon names can be obtained at: https://cfpb.github.io/capital-framework/components/cf-icons/. Examples: linkedin-square, facebook-square, etc.', label=b'H4 heading icon', required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(blank=True, required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False))])))]))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='AskCategoryPages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, to='v1.CFGOVPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='v1_askcategorypages_items', to='taggit.Tag')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='ask_categories',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text=b'A comma separated list of categories', through='v1.AskCategoryPages', to='taggit.Tag', verbose_name=b'Categories'),
        ),
    ]