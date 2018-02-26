from datetime import datetime

from django.contrib.syndication.views import Feed

from django.utils.feedgenerator import (
    Rss201rev2Feed
)

from django.utils.xmlutils import SimplerXMLGenerator

from wagtail.wagtailcore.url_routing import RouteResult

from jobmanager.models import JobListingPage

import pytz

import os

eastern = pytz.timezone('US/Eastern')


class FilterableFeed(Feed):
    item_guid_is_permalink = False

    def __init__(self, page, context):
        self.page = page
        self.context = context

    def link(self):
        return self.page.full_url

    def title(self):
        return "%s | Consumer Financial Protection Bureau" % self.page.title

    def items(self):
        posts = self.context['filter_data']['page_set']
        return posts

    def item_link(self, item):
        return item.full_url

    def item_pubdate(self, item):
        # this seems to require a datetime
        item_date = item.date_published
        naive = datetime.combine(item_date, datetime.min.time())
        return eastern.localize(naive)

    def item_description(self, item):
        return item.preview_description

    def item_categories(self, item):
        categories = [cat.get_name_display() for cat in item.categories.all()]
        tags = [tag.name for tag in item.tags.all()]
        return categories + tags

    def item_guid(self, item):
        return "%s<>consumerfinance.gov" % item.page_ptr_id


class FilterableFeedPageMixin(object):

    def route(self, request, path_components):
        if len(path_components) == 1 and path_components[0] == 'feed':
            return RouteResult(self, kwargs={'format': 'rss'})

        return super(FilterableFeedPageMixin,
                     self).route(request, path_components)

    def serve(self, request, format='html'):
        if format == 'rss':
            context = self.get_context(request)
            return FilterableFeed(self, context)(request)
        else:
            return super(FilterableFeedPageMixin, self).serve(request)


class CustomFeedGenerator(Rss201rev2Feed):
    mime_type = 'application/xml'

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement("source", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        handler.endElement("source")

    def write_items(self, handler):
        for item in self.items:
            handler.startElement('job', self.item_attributes(item))
            self.add_item_elements(handler, item)
            handler.endElement("job")

    def add_root_elements(self, handler):
        # Add root elements here
        handler.addQuickElement("publisher", self.feed['title'])
        handler.addQuickElement("publisherurl", self.feed['link'])

    def add_item_elements(self, handler, item):
        for x in item.keys():
            if x not in ['link', 'unique_id'] and item[x]:
                handler.startElement(x, {})
                content = '<![CDATA['
                content += (item[x].decode('utf-8') if x == 'url' else item[x])
                content += ']]>'
                handler._write(content)
                handler.endElement(x)


class IndeedFeed(Feed):
    feed_type = CustomFeedGenerator

    def link(self):
        return "https://www.consumerfinance.gov"

    def title(self):
        return "Consumer Financial Protection Bureau"

    def items(self):
        jobs = JobListingPage.objects.filter(live=True)
        return jobs

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        return unicode(item.generate_description())

    def item_number(self, item):
        link = item.usajobs_application_links.first()
        if link:
            return os.path.basename(os.path.normpath(link.url))

    def salary(self, item):
        return unicode('${:,.0f}-${:,.0f} per year'.format(
            item.salary_min, item.salary_max
        ))

    def item_extra_kwargs(self, item):
        """
        Returns an extra keyword arguments dictionary that is used with
        the 'add_item' call of the feed generator.
        Add the fields of the item, to be used by the custom feed generator.
        """

        extra_kwargs = {
            'company': u'Consumer Financial Protection Bureau',
            'url': item.full_url,
            'date': unicode(item.open_date.strftime('%a, %d %b %Y')),
            'referencenumber': self.item_number(item),
            'salary': self.salary(item),
            'country': unicode('US'),
        }
        if hasattr(item.location, 'office'):
            city = item.location.cities.first()
            if city:
                if city.state.abbreviation == 'DC':
                    extra_kwargs['city'] = unicode(city)
                else:
                    extra_kwargs['city'] = unicode(city.name)
                    extra_kwargs['state'] = unicode(city.state.abbreviation)
            else:
                location = unicode(item.location).split(', ')
                extra_kwargs['city'] = location[0]
                extra_kwargs['state'] = location[1]
        # Need to find out how to format multiple cities for regions
        return extra_kwargs


class GlassdoorFeedGenerator(Rss201rev2Feed):
    mime_type = 'application/xml'

    def add_item_elements(self, handler, item):
        for x in item.keys():
            if x not in ['link'] and item[x]:
                handler.addQuickElement(x, item[x])


class GlassdoorFeed(Feed):
    feed_type = GlassdoorFeedGenerator

    def link(self):
        return "https://www.consumerfinance.gov"

    def title(self):
        return "Consumer Financial Protection Bureau"

    def items(self):
        jobs = JobListingPage.objects.filter(live=True)
        return jobs

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        return item.generate_description()

    def item_guid(self, item):
        link = item.usajobs_application_links.first()
        if link:
            return os.path.basename(os.path.normpath(link.url))

    def salary(self, item):
        return unicode('${:,.0f}-${:,.0f} per year'.format(
            item.salary_min, item.salary_max
        ))

    def item_extra_kwargs(self, item):
        """
        Returns an extra keyword arguments dictionary that is used with
        the 'add_item' call of the feed generator.
        Add the fields of the item, to be used by the custom feed generator.
        """
        extra_kwargs = {
            'company': u'Consumer Financial Protection Bureau',
            'url': item.full_url,
            'date': unicode(item.open_date.strftime('%a, %d %b %Y')),
            'salary': self.salary(item),
            'country': unicode('US'),
        }
        if hasattr(item.location, 'office'):
            city = item.location.cities.first()
            if city:
                if city.state.abbreviation == 'DC':
                    extra_kwargs['city'] = unicode(city)
                else:
                    extra_kwargs['city'] = unicode(city.name)
                    extra_kwargs['state'] = unicode(city.state.abbreviation)
            else:
                location = unicode(item.location).split(', ')
                extra_kwargs['city'] = location[0]
                extra_kwargs['state'] = location[1]
        return extra_kwargs
