import json
import os
import shutil
import tempfile

from mock import patch
from unittest import TestCase

from legacy.housing_counselor.generator import generate_counselor_json


class TestGeneratorCounselorJson(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        patched = patch('legacy.housing_counselor.generator.print_')
        patched.start()
        self.addCleanup(patched.stop)

        self.counselors = [
            {'agc_ADDR_LATITUDE': 120, 'agc_ADDR_LONGITUDE': 98},
            {'agc_ADDR_LATITUDE': 125, 'agc_ADDR_LONGITUDE': 99},
        ]

        self.zipcodes = {
            '20001': (115.5, 97.5),
            '20002': (130.3, 100.1),
        }

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_generate_creates_json_files(self):
        generate_counselor_json(self.counselors, self.zipcodes, self.tempdir)
        self.assertEqual(
            os.listdir(self.tempdir),
            ['20001.json', '20002.json']
        )

    def test_generate_creates_proper_json(self):
        generate_counselor_json(self.counselors, self.zipcodes, self.tempdir)
        with open(os.path.join(self.tempdir, '20001.json')) as f:
            data = json.load(f)

        self.assertEqual(data, {
            'zip': {
                'lat': 115.5,
                'lng': 97.5,
                'zipcode': '20001',
            },
            'counseling_agencies': [
                {
                    'agc_ADDR_LATITUDE': 120,
                    'agc_ADDR_LONGITUDE': 98,
                    'distance': 311.35243783709234,
                },
                {
                    'agc_ADDR_LATITUDE': 125,
                    'agc_ADDR_LONGITUDE': 99,
                    'distance': 658.4536705140896,
                },
            ],
        })
