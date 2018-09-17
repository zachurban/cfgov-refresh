from __future__ import absolute_import
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.wagtailcore import blocks

from ask_cfpb.models.django import Answer
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules


class AskMetadata(blocks.StructBlock):
    answer_id = blocks.IntegerBlock(
        required=True,
        label='Answer ID',
        help_text='ID for the Ask CFPB Answer you wish to pull in data from.'
    )

    def render(self, value, context=None):
        print context
        answer = Answer.objects.get(id=value['answer_id'])
        value['snippet'] = answer.snippet
        value['categories'] = answer.category.all()
        value['subcategories'] = answer.subcategory.all()
        value['related_questions'] = answer.related_questions.all()
        template = '_includes/organisms/ask-metadata.html'
        return render_to_string(template, value)


class AskHeadingLevelBlock(blocks.ChoiceBlock):
    choices = [
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('b', 'bold'),
    ]
    classname = 'heading-level-block'


class AskHeadingBlock(blocks.StructBlock):
    text = v1_blocks.HeadingTextBlock(required=False)
    level = v1_blocks.HeadingLevelBlock(default='h2')

    class Meta:
        classname = 'ask-heading-block'
        icon = 'title'
        template = '_includes/blocks/heading.html'
        form_template = (
            'admin/form_templates/struct-with-block-wrapper-classes.html'
        )


class AllTextItem(blocks.StructBlock):
    answer_id = blocks.IntegerBlock(
        required=False,
        label='Answer ID',
        help_text='ID for the Ask CFPB Answer you wish to pull data from.'
    )
    heading = blocks.CharBlock(
        required=False,
        help_text=('Enter content for the heading text. If you have selected'
                   ' an Ask answer, the heading will default to its statement '
                   ' field unless you override it by entering custom '
                   ' content here.')
    )
    heading_level = AskHeadingLevelBlock(
        required=False,
        default='h4'
    )
    body = blocks.TextBlock(
        required=True,
        help_text=('Enter body text for this item. This field should be '
                   'filled out even if you have selected an Ask answer.'))
    link_text = blocks.CharBlock(required=True,)
    page_link = blocks.PageChooserBlock(
        required=False,
        help_text=('If you have not specified an Ask answer above, '
                   'use this to link to a page in Wagtail.'),
        label='Page'
    )
    external_link = blocks.CharBlock(
        required=False,
        max_length=1000,
        label='Direct URL',
        help_text=('Enter url for page outside Wagtail. This will only '
                   'be used if there is no page or Ask answer selected '
                   'above.')
    )

    def get_context(self, value, parent_context=None):
        ctx = super(AllTextItem, self).get_context(
            value, parent_context=parent_context)
        if value['answer_id']:
            try:
                answer = Answer.objects.get(id=value['answer_id'])
            except Exception:
                return
            ctx['page_link'] = answer.english_page \
                if answer.english_page else None
            ctx['heading'] = value['heading'] \
                if value['heading'] else answer.statement           
        else:
            for x in ['page_link', 'external_link',
                      'heading', 'heading_level']:
                ctx[x] = value[x]
        ctx['body'] = value['body']
        ctx['link_text'] = value['link_text']
        ctx['heading_level'] = value['heading_level']
        return ctx

    def clean(self, value):
        cleaned = super(AllTextItem, self).clean(value)

        if cleaned.get('answer_id'):
            try:
                answer = Answer.objects.get(id=cleaned['answer_id'])
            except ObjectDoesNotExist:
                raise ValidationError(
                    'Validation error in TextItem: '
                    'Ask answer does not exist',
                    params={'answer_id': ErrorList([
                        'Answer with given id does not exist.'
                    ])}
                )

        return cleaned

    class Meta:
        template = '_includes/ask/ask-text-item.html'


class AllLinkItem(blocks.StructBlock):
    answer_id = blocks.IntegerBlock(
        required=False,
        label='Answer ID',
        help_text='ID for the Ask CFPB Answer you wish to pull data from.'
    )
    link_text = blocks.CharBlock(
        required=False,
        help_text=('Link text will default to the statement field '
                   'of the answer you have selected '
                   'unless you override it by entering custom content '
                   'here.'))
    page_link = blocks.PageChooserBlock(
        required=False,
        help_text=('If you have not specified an Ask answer above, '
                   'use this to link to a page in Wagtail.'),
        label='Page'
    )
    external_link = blocks.CharBlock(
        required=False,
        max_length=1000,
        label='Direct URL',
        help_text='Enter url for page outside Wagtail. This will only '
                  'be used if there is no page or Ask answer selected above.'
    )

    def get_context(self, value, parent_context=None):
        ctx = super(AllLinkItem, self).get_context(
            value, parent_context=parent_context)
        print parent_context
        if value['answer_id']:
            try:
                answer = Answer.objects.get(id=value['answer_id'])
                if answer.english_page:
                    ctx['page_link'] = answer.english_page
                ctx['link_text'] = value['link_text'] \
                    if value['link_text'] else answer.statement
            except Exception:
                return  
        else:
            for x in ['link_text', 'page_link', 'external_link']:
                ctx[x] = value[x]
        return ctx
 
    def clean(self, value):
        cleaned = super(AllLinkItem, self).clean(value)

        if cleaned.get('answer_id'):
            try:
                answer = Answer.objects.get(id=cleaned['answer_id'])
            except ObjectDoesNotExist:
                raise ValidationError(
                    'Validation error in LinkItem: '
                    'Ask answer does not exist',
                    params={'answer_id': ErrorList([
                        'Answer with given id does not exist.'
                    ])}
                )

        return cleaned

    class Meta:
        template = '_includes/ask/ask-link-item.html'


class SummaryCombinedColumn(blocks.StructBlock):
    heading = AskHeadingBlock(
        classname="testing",
        required=False,
        default={'level': 'h3'})
    links = blocks.ListBlock(AllTextItem())


class LinkCombinedColumn(blocks.StructBlock):
    heading = AskHeadingBlock(
        classname="testing",
        required=False,
        default={'level': 'h3'})
    links = blocks.ListBlock(AllLinkItem())


class TextVsLinkBlock(blocks.StructBlock):
    heading = AskHeadingBlock(required=False,)
    intro = blocks.RichTextBlock(required=False)
    has_top_border = blocks.BooleanBlock(required=False)
    anchor_link = v1_blocks.AnchorLink()
    columns = blocks.StreamBlock(
        [
            ('ask_text_column', SummaryCombinedColumn()),
            ('ask_link_column', LinkCombinedColumn()),
            ('info_unit_column', molecules.InfoUnit())
        ]
    )

    class Meta:
        icon = 'title'
        template = '_includes/ask/ask-block.html'


class NonAskLinkItem(blocks.StructBlock):
    link_text = blocks.CharBlock(required=True,)
    page_link = blocks.PageChooserBlock(
        required=False,
        help_text='Link to a page in Wagtail.',
        label='Page'
    )
    external_link = blocks.CharBlock(
        required=False,
        max_length=1000,
        label='Direct URL',
        help_text='Enter url for page outside Wagtail. This will only '
                  'be used if there is no page selected.'
    )

    def get_context(self, value, parent_context=None):
        return value

    class Meta:
        template = '_includes/ask/ask-link-item.html'


class AskLinkItem(blocks.StructBlock):
    answer_id = blocks.IntegerBlock(
        required=True,
        label='Answer ID',
        help_text='ID for the Ask CFPB Answer you wish to pull data from.'
    )
    link_text = blocks.CharBlock(
        required=False,
        help_text=('Link text will default to the statement field '
                   'of the answer you have selected unless you '
                   'override it by entering custom content here.')
    )

    def get_context(self, value, parent_context=None):
        ctx = super(AskLinkItem, self).get_context(
            value, parent_context=parent_context)
        try:
            answer = Answer.objects.get(id=value['answer_id'])
            ctx['answer'] = answer
            if answer.english_page:
                ctx['page_link'] = answer.english_page
            ctx['link_text'] = value['link_text'] \
                if value['link_text'] else answer.statement
            return ctx
        except Exception:
            return

    def clean(self, value):
        cleaned = super(AskLinkItem, self).clean(value)

        if cleaned.get('answer_id'):
            try:
                answer = Answer.objects.get(id=cleaned['answer_id'])
            except ObjectDoesNotExist:
                raise ValidationError(
                    'Validation error in LinkItem: '
                    'Ask answer does not exist',
                    params={'answer_id': ErrorList([
                        'Answer with given id does not exist.'
                    ])}
                )

        return cleaned

    class Meta:
        template = '_includes/ask/ask-link-item.html'


class LinkColumn(blocks.StructBlock):
    heading = AskHeadingBlock(required=False, default={'level': 'h3'})
    links = blocks.StreamBlock(
        [
            ('ask_item', AskLinkItem()),
            ('link_item', NonAskLinkItem())
        ]
    )


class NonAskTextItem(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    heading_level = AskHeadingLevelBlock(required=True, default='h4')
    body = blocks.TextBlock(required=True,
                            help_text=('Enter body text for this item.'))
    link_text = blocks.CharBlock(required=True,)
    page_link = blocks.PageChooserBlock(
        required=False,
        help_text='Link to a page in Wagtail.',
        label='Page'
    )
    external_link = blocks.CharBlock(
        required=False,
        max_length=1000,
        label='Direct URL',
        help_text='Enter url for page outside Wagtail. This will only '
                  'be used if there is no page selected.'
    )

    def get_context(self, value, parent_context=None):
        return value

    class Meta:
        template = '_includes/ask/ask-text-item.html'


class AskTextItem(blocks.StructBlock):
    answer_id = blocks.IntegerBlock(
        required=True,
        label='Answer ID',
        help_text='ID for the Ask CFPB Answer you wish to pull data from.'
    )
    heading = blocks.CharBlock(
        required=False,
        help_text=('Heading will default to the statement field of '
                   'the answer you have selected unless you override '
                   'it by entering custom content here.')
    )
    heading_level = AskHeadingLevelBlock(required=True, default='h4')
    body = blocks.TextBlock(
        required=True,
        help_text=('Enter body text for this item.'))
    link_text = blocks.CharBlock(
        required=True,)

    def get_context(self, value, parent_context=None):
        ctx = super(AskTextItem, self).get_context(
            value, parent_context=parent_context)
        try:
            answer = Answer.objects.get(id=value['answer_id'])
            ctx['answer'] = answer
            if answer.english_page:
                ctx['page_link'] = answer.english_page
            ctx['heading'] = value['heading'] \
                if value['heading'] else answer.statement
            ctx['body'] = value['body']
            ctx['link_text'] = value['link_text']
            ctx['heading_level'] = value['heading_level']
            return ctx
        except Exception:
                return

    def clean(self, value):
        cleaned = super(AskTextItem, self).clean(value)

        if cleaned.get('answer_id'):
            try:
                answer = Answer.objects.get(id=cleaned['answer_id'])
            except ObjectDoesNotExist:
                raise ValidationError(
                    'Validation error in TextItem: '
                    'Ask answer does not exist',
                    params={'answer_id': ErrorList([
                        'Answer with given id does not exist.'
                    ])}
                )

        return cleaned


    class Meta:
        template = '_includes/ask/ask-text-item.html'


class TextColumn(blocks.StructBlock):
    heading = AskHeadingBlock(
        required=False,
        default={'level': 'h3'})
    links = blocks.StreamBlock(
        [
            ('ask_item', AskTextItem()),
            ('text_item', NonAskTextItem()),
        ]
    )


class TextAndLinkBlock(blocks.StructBlock):
    heading = AskHeadingBlock(required=False,)
    intro = blocks.RichTextBlock(required=False)
    has_top_border = blocks.BooleanBlock(required=False)
    anchor_link = v1_blocks.AnchorLink()

    columns = blocks.StreamBlock(
        [
            ('ask_link_column', LinkColumn()),
            ('ask_text_column', TextColumn()),
            ('info_unit_column', molecules.InfoUnit())
        ]
    )

    class Meta:
        icon = 'title'
        template = '_includes/ask/ask-block.html'
