from __future__ import print_function

import base64
import csv
import os
import re
import requests
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from django.utils.functional import cached_property
from tempfile import TemporaryFile
from unipath import Path

from hud_api_replace.views import export_html


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Initialize PDFreactor.
        self.pdfreactor

        # Download list of zip codes.
        print('downloading zip codes')
        zipcodes = sorted(set(self.generate_zip_codes()))
        print('downloaded {} zip codes'.format(len(zipcodes)))

        # Iterate over all zip codes and generate PDFs.
        request = HttpRequest()
        for zipcode in zipcodes:
            print('generating HTML for {}'.format(zipcode))
            response = export_html(request, zipcode)
            print('saving PDF for {}'.format(zipcode))
            self.save_pdf(zipcode, response.content)

    def generate_zip_codes(self):
        census_data_url = (
            'http://www2.census.gov'
            '/geo/docs/maps-data/data/rel/zcta_tract_rel_10.txt'
        )

        response = requests.get(census_data_url, stream=True)
        response.raise_for_status()

        with TemporaryFile() as f:
            for chunk in response:
                f.write(chunk)

            f.seek(0)

            reader = csv.DictReader(f)
            for line in reader:
                yield line['ZCTA5']

    def save_pdf(self, zipcode, html):
        # Need to modify template to include image from data URI.
        img_pattern = r'<img[^>]*\ src="([^"]+)"'

        def replace_img_src(match):
            return re.sub(match.group(1), self.logo_img, match.group(0))

        html = re.sub(img_pattern, replace_img_src, html)

        # Render PDF.
        pdf = self.pdfreactor.renderDocumentFromContent(html)

        filename = '{}.pdf'.format(zipcode)
        with open(filename, 'wb') as f:
            f.write(pdf)

        print('saved {}'.format(filename))

    @cached_property
    def pdfreactor(self):
        sys.path.append(os.environ['PDFREACTOR_LIB'])
        from PDFreactor import PDFreactor

        reactor = PDFreactor()

        reactor.setLicenseKey(os.environ['PDFREACTOR_LICENSE'])
        reactor.setAuthor('CFPB')
        reactor.setAddTags(True)
        reactor.setAddBookmarks(True)

        # Add custom CSS.
        reactor.addUserStyleSheet(self.css, '', '', '')

        # Ensure that reactor can be connected to.
        reactor.renderDocumentFromContent('')

        return reactor

    @cached_property
    def css(self):
        css_filename = Path(
            settings.REPOSITORY_ROOT,
            'cfgov/legacy/static/nemo/_/c/hud-hca-api-pdf-style.css'
        )

        with open(css_filename, 'rb') as f:
            return f.read()

    @cached_property
    def logo_img(self):
        image_filename = Path(
            settings.REPOSITORY_ROOT,
            'cfgov/legacy/static/nemo/_/img/logo.png'
        )

        with open(image_filename, 'rb') as f:
            data = base64.b64encode(f.read())

        return 'data:image/png;base64,{}'.format(data)
