from __future__ import absolute_import, unicode_literals

import re


class HousingCounselorCleaner(object):
    """Class that cleans raw counselor data from HUD."""
    REQUIRED_COUNSELOR_KEYS = {
        'adr1', 'adr2', 'agc_ADDR_LATITUDE', 'agc_ADDR_LONGITUDE', 'city',
        'email', 'languages', 'nme', 'phone1', 'services', 'statecd', 'weburl',
        'zipcd',
    }

    def __init__(self, fetcher):
        self.fetcher = fetcher

    def clean(self):
        """Returns a cleaned set of HUD housing counselors."""
        return map(self.clean_counselor, self.fetcher.counselors)

    def clean_counselor(self, counselor):
        """Cleans a single housing counselor."""
        counselor = dict(counselor)

        if not self.REQUIRED_COUNSELOR_KEYS.issubset(set(counselor.keys())):
            raise ValueError('missing keys in counselor')

        self.replace_abbreviations(
            counselor,
            'languages',
            self.fetcher.languages
        )

        self.replace_abbreviations(
            counselor,
            'services',
            self.fetcher.services
        )

        for key in ('agc_ADDR_LATITUDE', 'agc_ADDR_LONGITUDE'):
            counselor[key] = self.float_or_none(counselor[key])

        for key in ('city', 'nme'):
            counselor[key] = self.title_case(counselor[key])

        counselor['email'] = self.reformat_email(counselor['email'])
        counselor['weburl'] = self.reformat_weburl(counselor['weburl'])

        return counselor

    @staticmethod
    def replace_abbreviations(counselor, key, lookups):
        """Replace abbreviations in a counselor key with names."""
        abbreviations = counselor[key]
        counselor[key] = map(
            lambda k: lookups[k],
            abbreviations.split(',') if abbreviations else []
        )

    @staticmethod
    def float_or_none(s):
        """Convert a string to a float."""
        if s:
            return float(s)

    @staticmethod
    def title_case(s):
        """Convert a string to have title case."""
        if not s:
            return None

        s = s.lower()
        parts = s.split(' ')
        lower_case = (
            'a', 'an', 'and', 'as', 'at', 'by', 'for', 'in', 'of', 'on', 'or',
            'the', 'to', 'with'
        )

        parts[0] = parts[0].title()
        parts = map(
            lambda part: part.title() if part not in lower_case else part,
            parts
        )

        return ' '.join(parts)

    @staticmethod
    def reformat_weburl(s):
        """Convert invalid URLs to null."""
        s = (s or '').strip()

        if s and '.' in s and 'notavailable' not in s:
            match = re.match(r'^http(s)?://', s)
            if not match:
                s = 'http://' + s

            return s

    @staticmethod
    def reformat_email(s):
        s = (s or '').strip()
        if '.' in s and '@' in s:
            return s
