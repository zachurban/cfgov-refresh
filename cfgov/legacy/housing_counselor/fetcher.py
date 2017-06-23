from __future__ import absolute_import, unicode_literals

import requests

from django.utils.functional import cached_property
from six import print_


class HousingCounselorFetcher(object):
    """Download housing counselor data from HUD."""
    HUD_COUNSELORS_URL = (
        'https://data.hud.gov/Housing_Counselor/searchByLocation?'
        'Lat=38.8951&Long=-77.0367&Distance=5000'
    )

    HUD_LANGUAGES_URL = 'https://data.hud.gov/Housing_Counselor/getLanguages'
    HUD_SERVICES_URL = 'https://data.hud.gov/Housing_Counselor/getServices'

    @cached_property
    def housing_counselors(self):
        """Download HUD counselors within a radius centered on DC."""
        url = self.HUD_COUNSELORS_URL
        print_('Downloading HUD counselors from', url, flush=True)
        counselors = self.get_json_from_url(url)

        if not counselors:
            raise RuntimeError('Could not download HUD counselors')

        print_('Retrieved', len(counselors), 'counselors', flush=True)
        return counselors

    @cached_property
    def languages(self):
        """Download HUD language abbreviations and names."""
        return self.get_abbreviations(self.HUD_LANGUAGES_URL)

    @cached_property
    def services(self):
        """Download HUD service abbreviations and names."""
        return self.get_abbreviations(self.HUD_SERVICES_URL)

    @classmethod
    def get_abbreviations(cls, url):
        """Retrieve HUD abbreviations from a URL."""
        print_('Downloading abbreviations from', url, flush=True)
        values = cls.get_json_from_url(url)
        return dict((lang['key'], lang['value']) for lang in values)

    @staticmethod
    def get_json_from_url(url):
        """Retrieve JSON from a URL, raising on failure."""
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
