from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, ObjectList,
    StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailsearch import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class ArticlePage(CFGOVPage):
    tag = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=500, blank=True)
    limit = models.CharField(
        max_length=3,
        default='3',
        help_text='Limit list to this number of items'
    )
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('well', organisms.Well()),
        ('feedback', v1_blocks.Feedback()),
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('third_width_link_blob_group', organisms.ThirdWidthLinkBlobGroup()),
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            FieldPanel('tag', classname='full'),
            FieldPanel('category', classname='full'),
            FieldPanel('limit', classname='full'),
        ], heading='Related answers', classname='collapsible'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'article-page/index.html'

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('content'),
        index.SearchField('header')
    ]

    def get_context(self, request, *args, **kwargs):
        from ask_cfpb.models.pages import AnswerPage
        answers = AnswerPage.objects.filter(
            ask_categories__name__in=[self.category]).filter(
            tags__name__in=[self.tag])[:self.limit]
        context = super(ArticlePage, self).get_context(
            request, *args, **kwargs
        )
        context.update({
            'answers': answers
        })
        return context
