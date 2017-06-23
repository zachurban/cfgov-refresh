from __future__ import absolute_import, unicode_literals

import responses

from mock import patch
from requests.exceptions import HTTPError
from unittest import TestCase

from legacy.housing_counselor.fetcher import HousingCounselorFetcher


class TestHousingCounselorFetcher(TestCase):
    def setUp(self):
        patched = patch('legacy.housing_counselor.fetcher.print_')
        patched.start()
        self.addCleanup(patched.stop)

    @responses.activate
    def test_get_json_from_url_calls_requests_get(self):
        responses.add(responses.GET, 'http://test.url', json={'foo': 'bar'})
        response = HousingCounselorFetcher.get_json_from_url('http://test.url')
        self.assertEquals(response, {'foo': 'bar'})

    @responses.activate
    def test_get_json_from_url_raises_on_requests_failure(self):
        responses.add(responses.GET, 'http://test.url', status=503)
        with self.assertRaises(HTTPError):
            HousingCounselorFetcher.get_json_from_url('http://test.url')

    @responses.activate
    def test_housing_counselors_requests_from_url(self):
        counselors = [
            {'a': 'b', 'c': 'd'},
            {'e': 'f', 'g': 'h'},
            {'i': 'j', 'k': 'l'},
        ]

        responses.add(
            responses.GET,
            HousingCounselorFetcher.HUD_COUNSELORS_URL,
            match_querystring=True,
            json=counselors
        )

        self.assertEqual(
            HousingCounselorFetcher().housing_counselors,
            counselors
        )

    @responses.activate
    def test_no_housing_counselors_raises_exception(self):
        responses.add(
            responses.GET,
            HousingCounselorFetcher.HUD_COUNSELORS_URL,
            match_querystring=True,
            body='[]'  # see https://github.com/getsentry/responses/issues/146
        )

        with self.assertRaises(RuntimeError):
            HousingCounselorFetcher().housing_counselors

    @responses.activate
    def check_method_requests_json_and_converts_to_dict(self, method, url):
        responses.add(
            responses.GET,
            url,
            json=[
                {'key': 'a', 'value': 'b'},
                {'key': 'c', 'value': 'd'},
                {'key': 'e', 'value': 'f'},
            ]
        )

        self.assertEqual(
            method(),
            {
                'a': 'b',
                'c': 'd',
                'e': 'f',
            }
        )

    def test_languages_requests_from_url_and_creates_dict(self):
        self.check_method_requests_json_and_converts_to_dict(
            lambda: HousingCounselorFetcher().languages,
            HousingCounselorFetcher.HUD_LANGUAGES_URL
        )

    def test_services_requests_from_url_and_creates_dict(self):
        self.check_method_requests_json_and_converts_to_dict(
            lambda: HousingCounselorFetcher().services,
            HousingCounselorFetcher.HUD_SERVICES_URL
        )
