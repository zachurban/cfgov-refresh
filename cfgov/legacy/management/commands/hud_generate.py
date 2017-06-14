from __future__ import print_function

import csv
import json
import math
import os

from django.core.management.base import BaseCommand
from django.db import connection
from django.template import loader


def assert_counselor_data_exists():
    """Assert that counselor data exists in the database."""
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM hud_api_replace_counselingagency')
    count = int(cursor.fetchone()[0])

    if not count:
        raise RuntimeError('missing counselor data')

    print('{} housing counselor(s) in database'.format(count))


def load_zipcodes(filename):
    """Load zipcode location data from Census gazetteer file.

    See https://www.census.gov/geo/maps-data/data/gazetteer2016.html

    Returns a tuple of strings: (zipcode, latitude_degrees, longitude_degrees)
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)

        return [(row[0], row[5].strip(), row[6].strip()) for row in reader]


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def query_counselors(latitude_degrees, longitude_degrees, limit=10):
    """Find housing counselors closest to a location.

    Requires existing dataset load from django-hud.

    Uses simplified algorithm to determine proximity based on latitude and
    longitude, described at https://stackoverflow.com/q/1916953.
    """
    earth_radius_in_miles = 3959

    if connection.vendor == 'sqlite':
        connection.connection.create_function('acos', 1, math.acos)
        connection.connection.create_function('cos', 1, math.cos)
        connection.connection.create_function('radians', 1, math.radians)
        connection.connection.create_function('sin', 1, math.sin)

    sql = """
SELECT
    *,
    (%s * acos(
        cos(radians(CAST(%s AS FLOAT))) *
        cos(radians(CAST(agc_ADDR_LATITUDE AS FLOAT))) *
        cos(
            radians(CAST(agc_ADDR_LONGITUDE AS FLOAT)) -
            radians(CAST(%s AS FLOAT))
        ) +
        sin(radians(CAST(%s AS FLOAT))) *
        sin(radians(CAST(agc_ADDR_LATITUDE AS FLOAT)))
    )) AS distance
FROM hud_api_replace_counselingagency
ORDER BY distance ASC
LIMIT %s
"""

    cursor = connection.cursor()
    cursor.execute(sql, [
        earth_radius_in_miles,
        latitude_degrees,
        longitude_degrees,
        latitude_degrees,
        limit
    ])

    return dictfetchall(cursor)


class HUDGenerator(object):
    template_name = 'hud/housing_counselor_pdf_selfcontained.html'

    def __init__(self, target):
        self.target = target
        self.template = loader.get_template(self.template_name)

    def generate(self, zipcodes):
        for zipcode, data in self.generate_zipcode_data(zipcodes):
            self.write_json(zipcode, data)
            self.write_pdf(zipcode, data)

    @staticmethod
    def generate_zipcode_data(zipcodes):
        for zipcode, latitude_degrees, longitude_degrees in zipcodes:
            counselors = query_counselors(latitude_degrees, longitude_degrees)

            zipcode_data = {
                'zip': {
                    'zipcode': zipcode,
                    'lat': float(latitude_degrees),
                    'lng': float(longitude_degrees),
                },
                'counseling_agencies': counselors,
            }

            yield zipcode, zipcode_data

    def write_json(self, zipcode, data):
        json_filename = os.path.join(self.target, '{}.json'.format(zipcode))

        with open(json_filename, 'w') as f:
            f.write(json.dumps(data))

    def write_pdf(self, zipcode, data):
        html_filename = os.path.join(self.target, '{}.html'.format(zipcode))

        html = self.template.render({
            'zipcode': zipcode,
            'zipcode_valid': True,
            'api_json': data,
        })

        with open(html_filename, 'w') as f:
            f.write(html.encode('utf-8'))


class Command(BaseCommand):
    help = 'Generate bulk housing counselor data'

    def add_arguments(self, parser):
        parser.add_argument('zipcode_filename')
        parser.add_argument('target')

    def handle(self, *args, **options):
        assert_counselor_data_exists()

        zipcode_filename = options['zipcode_filename']
        zipcodes = load_zipcodes(zipcode_filename)
        print('loaded {} zipcodes from {}'.format(
            len(zipcodes),
            zipcode_filename
        ))

        target = options['target']
        print('generating files into {}'.format(target))

        generator = HUDGenerator(target)
        generator.generate(zipcodes)
