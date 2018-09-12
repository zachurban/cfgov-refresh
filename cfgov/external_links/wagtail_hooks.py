from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from external_links.views import search


try:
    from django.urls import reverse
except ImportError:  # pragma: no cover; fallback for Django <1.10
    from django.core.urlresolvers import reverse

try:
    from wagtail.admin.menu import MenuItem
    from wagtail.core import hooks  # pragma: no cover
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailadmin.menu import MenuItem
    from wagtail.wagtailcore import hooks



@hooks.register('register_admin_urls')
def register_external_links_url():
    return [url(r'^external-links/$', search, name='external-links'), ]


@hooks.register('register_admin_menu_item')
def register_external_links_menu():
    return MenuItem('External Links',
                    reverse('external-links'),
                    classnames='icon icon-cogs',
                    order=10000)
