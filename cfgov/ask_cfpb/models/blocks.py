from __future__ import absolute_import

from django.template.loader import render_to_string

from wagtail.wagtailcore import blocks

from ask_cfpb.models.django import Answer


class AskMetadata(blocks.StructBlock):
    answer_id = blocks.IntegerBlock(
        required=True,
        label='Answer ID',
        help_text='ID for the Ask CFPB Answer you wish to pull in data from.'
    )

    def render(self, value, context=None):
        answer = Answer.objects.get(id=value['answer_id'])
        value['snippet'] = answer.snippet
        value['categories'] = answer.category.all()
        value['subcategories'] = answer.subcategory.all()
        value['related_questions'] = answer.related_questions.all()
        template = '_includes/organisms/ask-metadata.html'
        return render_to_string(template, value)
