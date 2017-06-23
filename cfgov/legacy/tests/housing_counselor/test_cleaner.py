from __future__ import absolute_import, unicode_literals

from itertools import repeat
from mock import Mock
from unittest import TestCase

from legacy.housing_counselor.cleaner import HousingCounselorCleaner


class TestHousingCounselorCleaner(TestCase):
    def mock_counselor(self, **kwargs):
        counselor = {
            'adr1': '123 Main St',
            'adr2': None,
            'agc_ADDR_LATITUDE': '123.45',
            'agc_ADDR_LONGITUDE': '-76.5',
            'city': 'Washington',
            'email': 'hello@domain.com',
            'languages': [],
            'nme': 'Name',
            'phone1': '202-555-1234',
            'services': [],
            'statecd': 'DC',
            'weburl': 'example.com',
            'zipcd': '20001',
        }
        counselor.update(kwargs)
        return counselor

    def test_clean_no_counselors_returns_empty_list(self):
        fetcher = Mock(counselors=[])
        cleaner = HousingCounselorCleaner(fetcher)
        self.assertEqual(cleaner.clean(), [])

    def test_clean_cleans_list_from_fetcher(self):
        fetcher = Mock(counselors=repeat(self.mock_counselor(), 10))
        cleaner = HousingCounselorCleaner(fetcher)
        cleaned = cleaner.clean()
        self.assertEqual(len(cleaned), 10)

    def test_clean_counselor_missing_keys_raises_valueerror(self):
        fetcher = Mock()
        cleaner = HousingCounselorCleaner(fetcher)
        with self.assertRaises(ValueError):
            cleaner.clean_counselor({})

    def test_clean_counselor_cleans_valid_data(self):
        counselor = self.mock_counselor(
            agc_ADDR_LATITUDE='-34.56',
            agc_ADDR_LONGITUDE='99.79',
            city='mycity',
            email=' foo@bar.com ',
            extra_key='something',
            languages='EN,SP',
            nme='MYNAME',
            services='B,F',
            weburl='foo.com',
        )

        fetcher = Mock(
            languages={'EN': 'English', 'SP': 'Spanish'},
            services={'B': 'Bar', 'F': 'Foo'}
        )

        cleaner = HousingCounselorCleaner(fetcher)
        cleaned = cleaner.clean_counselor(counselor)

        self.assertEqual(cleaned['agc_ADDR_LATITUDE'], -34.56)
        self.assertEqual(cleaned['agc_ADDR_LONGITUDE'], 99.79)
        self.assertEqual(cleaned['city'], 'Mycity')
        self.assertEqual(cleaned['email'], 'foo@bar.com')
        self.assertEqual(cleaned['nme'], 'Myname')
        self.assertEqual(cleaned['weburl'], 'http://foo.com')

    def test_replace_abbreviations_converts_to_dict(self):
        counselor = {'x': 'q', 'items': 'f,b'}

        HousingCounselorCleaner.replace_abbreviations(
            counselor,
            'items',
            {'b': 'bar', 'f': 'foo'}
        )

        self.assertEqual(counselor, {'x': 'q', 'items': ['foo', 'bar']})

    def test_float_or_none_none_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.float_or_none(None))

    def test_float_or_none_empty_string_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.float_or_none(''))

    def test_float_or_none_invalid_raises_valueerror(self):
        with self.assertRaises(ValueError):
            HousingCounselorCleaner.float_or_none('foo')

    def test_float_or_none_positive_number(self):
        self.assertEqual(HousingCounselorCleaner.float_or_none('12.34'), 12.34)

    def test_float_or_none_negative_number(self):
        self.assertEqual(HousingCounselorCleaner.float_or_none('-9.8'), -9.8)

    def test_title_case_none_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.title_case(None))

    def test_title_case_empty_string_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.title_case(''))

    def test_title_case_multiple_words(self):
        self.assertEqual(
            HousingCounselorCleaner.title_case('SOME WORDS like tHiS'),
            'Some Words Like This'
        )

    def test_title_case_leaves_special_words_lowercase(self):
        self.assertEqual(
            HousingCounselorCleaner.title_case('HELLO FOR THE PEOPLE'),
            'Hello for the People'
        )

    def test_title_case_first_special_word_titlecase(self):
        self.assertEqual(
            HousingCounselorCleaner.title_case('of the people by the people'),
            'Of the People by the People'
        )

    def test_reformat_weburl_none_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.reformat_weburl(None))

    def test_reformat_weburl_empty_string_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.reformat_weburl(''))

    def test_reformat_weburl_invalid_returns_none(self):
        self.assertIsNone(
            HousingCounselorCleaner.reformat_weburl('foo bar')
        )

    def test_reformat_weburl_notavailable_returns_none(self):
        self.assertIsNone(
            HousingCounselorCleaner.reformat_weburl('www.notavailable.org')
        )

    def test_reformat_weburl_adds_http_if_not_present(self):
        self.assertEqual(
            HousingCounselorCleaner.reformat_weburl('www.domain.com'),
            'http://www.domain.com'
        )

    def test_reformat_weburl_keeps_http_if_present(self):
        url = 'http://www.domain.com'
        self.assertEqual(HousingCounselorCleaner.reformat_weburl(url), url)

    def test_reformat_weburl_keeps_https_if_present(self):
        url = 'https://www.domain.com'
        self.assertEqual(HousingCounselorCleaner.reformat_weburl(url), url)

    def test_reformat_weburl_keeps_complex_url(self):
        url = 'https://www.domain.com/path/to/page?query=string&foo=bar'
        self.assertEqual(HousingCounselorCleaner.reformat_weburl(url), url)

    def test_reformat_email_none_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.reformat_email(None))

    def test_reformat_email_empty_string_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.reformat_email(''))

    def test_reformat_email_valid_email_returned_properly(self):
        email = 'name@domain.com'
        self.assertEqual(HousingCounselorCleaner.reformat_email(email), email)

    def test_reformat_email_no_dot_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.reformat_email('foo@bar'))

    def test_reformat_email_no_at_returns_none(self):
        self.assertIsNone(HousingCounselorCleaner.reformat_email('foo.bar'))
