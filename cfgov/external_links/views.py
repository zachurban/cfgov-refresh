from itertools import chain

from django.shortcuts import render

from external_links.forms import ExternalLinksForm

from ask_cfpb.models.django import Answer
from v1.models.base import CFGOVPage
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.home_page import HomePage
from v1.models.learn_page import (
    AbstractFilterPage, DocumentDetailPage, LearnPage
)
from v1.models.landing_page import LandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.sublanding_page import SublandingPage


def queryset_content_header(cls, url):
    return cls.objects.raw(
        'SELECT * from v1_' + cls.__name__.lower() + ' WHERE content LIKE %s'
        ' OR header LIKE %s',
        [url, url])


def queryset(cls, url, column):
    return cls.objects.raw(
        'SELECT * from v1_' + cls.__name__.lower() + ' WHERE ' + column + ' LIKE %s',
        [url])


def search(request):
    if request.method == 'GET':
        return render(
            request, 'search.html',
            context={
                'form': ExternalLinksForm(),
            }
        )

    elif request.method == 'POST':
        form = ExternalLinksForm(request.POST)
        if not form.is_valid() or form.data['url'] == '':
            return render(
                request, 'search.html',
                context={
                    'form': form,
                }
            )

        url = '%' + form.data['url'] + '%'

        # Sidefoot lives on CFGOVPage
        cfgov_pages = queryset(CFGOVPage, url, 'sidefoot')

        # Content only lives on these pages
        blog_pages = queryset(BlogPage, url, 'content')
        legacy_blog_pages = queryset(LegacyBlogPage, url, 'content')
        document_detail_pages = queryset(DocumentDetailPage, url, 'content')
        learn_pages = queryset(LearnPage, url, 'content')

        # Header only lives on these pages
        abstract_filter_pages = queryset(AbstractFilterPage, url, 'header')
        home_pages = queryset(HomePage, url, 'header')

        # Content & header both live on these pages
        browse_pages = queryset_content_header(BrowsePage, url)
        browse_filterable_pages = queryset_content_header(BrowseFilterablePage, url)
        landing_pages = queryset_content_header(LandingPage, url)
        sublanding_filterable_pages = queryset_content_header(SublandingFilterablePage, url)
        sublanding_pages = queryset_content_header(SublandingPage, url)

        pages = chain(
            abstract_filter_pages, blog_pages,
            browse_filterable_pages, browse_pages,
            cfgov_pages, document_detail_pages, home_pages,
            landing_pages, learn_pages, legacy_blog_pages,
            sublanding_filterable_pages, sublanding_pages)

        answers = Answer.objects.raw(
            'SELECT * from ask_cfpb_answer WHERE answer LIKE %s OR '
            'answer_es LIKE %s',
            [url, url])

        return render(
            request, 'search.html',
            context={
                'form': form,
                'pages': pages,
                'answers': answers
            }
        )
