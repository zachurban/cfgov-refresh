import json

from v1.models import CFGOVPage
from v1 import parse_links
from django.test import RequestFactory
from wagtail.wagtailcore.models import Site



def run():
    count = 0
    default_site = Site.objects.get(is_default_site=True)
    urls = {}
    failed_pages = []
    for page in CFGOVPage.objects.all():
        page = page.specific
        if page.url and page.title != 'CFGov' and page.live:
            try:
                factory = RequestFactory()
                request = factory.get(page.url)
                request.site = default_site
                resp = page.serve(request)
                content = resp.rendered_content
                parsed_links = parse_links(content)
                for link in parsed_links:
                    if link in urls:
                        urls[link].append(page.url)
                    else:
                        urls[link] = [page.url]
            except:
                failed_pages.append(page.url)

    for url in urls:
        print "URL " + url
        print "Found in..."
        for page in urls[url]:
            print page
        print '---------'
    
    print "Did not process following pages:"
    for page in failed_pages:
        print page
