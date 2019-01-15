from __future__ import unicode_literals

import datetime
from six.moves import html_parser as HTMLParser

from django.http import HttpResponse
from django.utils import html

import unicodecsv

from ask_cfpb.models.django import (
    Answer, Audience, Category, NextStep, SubCategory
)
from ask_cfpb.models.pages import AnswerPage


html_parser = HTMLParser.HTMLParser()

HEADINGS = [
    'ASK_ID',
    'Question',
    'ShortAnswer',
    'Answer',
    'URL',
    'Live',
    'Redirect',
    'SpanishQuestion',
    'SpanishAnswer',
    'SpanishURL',
    'SpanishLive',
    'SpanishRedirect',
    'Topic',
    'SubCategories',
    'Audiences',
    'RelatedQuestions',
    'RelatedResources',
]


def clean_and_strip(data):
    unescaped = html_parser.unescape(data)
    return html.strip_tags(unescaped).strip()


def assemble_output():
    answers = Answer.objects.values()
    output_rows = []
    for answer in answers:
        output = {heading: '' for heading in HEADINGS}
        output['ASK_ID'] = answer['id']
        output['Question'] = answer['question']
        output['ShortAnswer'] = clean_and_strip(answer['snippet'])
        output['Answer'] = clean_and_strip(answer['answer'])
        output['SpanishQuestion'] = answer['question_es'].replace('\x81', '')
        output['SpanishAnswer'] = clean_and_strip(
            answer['answer_es']).replace('\x81', '')

        pages = AnswerPage.objects.filter(
            answer_base__id=answer['id']).values()
        for page in pages:
            if page['language'] == 'en':
                output['URL'] = page['url_path'].replace('/cfgov', '')
                output['Live'] = page['live']
                output['Redirect'] = page['redirect_to_id']
            elif page['language'] == 'es':
                output['SpanishURL'] = page['url_path'].replace('/cfgov', '')
                output['SpanishLive'] = page['live']
                output['SpanishRedirect'] = page['redirect_to_id']

        category = Category.objects.filter(
            answer__id=answer['id']).values('name').first()
        subcategories = SubCategory.objects.filter(
            answer__id=answer['id']).values('name')
        audiences = Audience.objects.filter(
            answer__id=answer['id']).values('name')
        next_step = NextStep.objects.filter(
            answer__id=answer['id']).values('title').first()
        related_questions = Answer.objects.get(
            id=answer['id']).related_questions.values('id')

        output['Topic'] = category['name'] if category else ''
        output['SubCategories'] = " | ".join(
            subcat['name'] for subcat in subcategories)
        output['Audiences'] = " | ".join(aud['name'] for aud in audiences)
        output['RelatedQuestions'] = " | ".join(
            ['{}'.format(a['id']) for a in related_questions])
        output['RelatedResources'] = next_step['title'] if next_step else ''
        output_rows.append(output)
    return output_rows


def export_questions(path='/tmp', http_response=False):
    """
    A script for exporting Ask CFPB Answer content
    to a CSV that can be opened easily in Excel.

    Run from within cfgov-refresh with:
    `python cfgov/manage.py runscript export_ask_data`

    CEE staffers use a version of Excel that can't easily import UTF-8
    non-ascii encodings. So we throw in the towel and encode the CSV
    with windows-1252.

    By default, the script will dump the file to `/tmp/`,
    unless a path argument is supplied,
    or http_response is set to True (for downloads via the Wagtail admin).
    A command that passes in path would look like this:
    `python cfgov/manage.py runscript export_ask_data --script-args [PATH]`
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = 'ask-cfpb-{}.csv'.format(timestamp)
    if http_response:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment;filename={}'.format(slug)
        write_questions_to_csv(response)
        return response
    file_path = '{}/{}'.format(path, slug).replace('//', '/')
    with open(file_path, 'w') as f:
        write_questions_to_csv(f)


def write_questions_to_csv(csvfile):
    writer = unicodecsv.writer(csvfile, encoding='windows-1252')
    writer.writerow(HEADINGS)
    for row in assemble_output():
            writer.writerow(
                [row.get(key) for key in HEADINGS])


def run(*args):
    if args:
        export_questions(path=args[0])
    else:
        export_questions()
