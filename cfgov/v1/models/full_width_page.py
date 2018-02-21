from wagtail.wagtailadmin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager


from wagtail.wagtailcore import blocks
from ..atomic_elements import molecules, organisms
from .base import CFGOVPage


class FullWidthPage(CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([
        ('content_block', organisms.ContentBlock()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('well', organisms.Well()),
        ('raw_html_block', blocks.RawHTMLBlock(
            label='Raw HTML block')),
        ('full_width_text', organisms.FullWidthText()),
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Footer'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'full-width-page/index.html'

    objects = PageManager()
