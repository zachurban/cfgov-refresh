from django.shortcuts import render
from django.views.generic import View

from external_links.forms import ExternalLinksForm

from ask_cfpb.models.pages import AnswerPage
from v1.models.base import CFGOVPage
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.home_page import HomePage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import (
    AbstractFilterPage, DocumentDetailPage, EventPage, LearnPage
)
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.sublanding_page import SublandingPage


class SearchView(View):
    template_name = 'search.html'
    # These are all v1 models that directly implement a visible part
    # of the Wagtail page, e.g. content, sidefoot, and header
    v1_page_models = [
        CFGOVPage, HomePage, AbstractFilterPage, BlogPage,
        BrowsePage, BrowseFilterablePage,
        DocumentDetailPage, EventPage,
        LegacyBlogPage, LearnPage, LandingPage,
        SublandingPage, SublandingFilterablePage,
    ]

    def get(self, request):
        return render(request, self.template_name, {
            'form': ExternalLinksForm()
        })

    def post(self, request):
        form = ExternalLinksForm(request.POST)
        url = form.data['url']
        pages = []

        for cls in self.v1_page_models:
            pages += list(cls.objects.search(url))

        pages += list(AnswerPage.objects.search(url, fields=[
            'answer', 'snippet'
        ]))

        num_results = len(pages)

        return render(request, self.template_name, {
            'form': form,
            'pages': pages,
            'num_results': num_results,
        })
