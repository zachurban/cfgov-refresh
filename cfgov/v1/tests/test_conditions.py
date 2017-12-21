from django.test import TestCase, RequestFactory

from wagtail.wagtailcore.models import Site, Page

from flags.conditions import RequiredForCondition

from v1.conditions import (
    page_primary_key_condition,
)


class PrimaryKeyConditionTestCase(TestCase):

    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.page = Page(slug='test-page', title='Test Page')
        self.site.root_page.add_child(instance=self.page)

        self.request = RequestFactory().get('/test-page')
        self.request.site = self.site

    def test_primary_key_valid_string(self):
        self.assertTrue(
            page_primary_key_condition(str(self.page.pk), self.request)
        )

    def test_primary_key_valid_int(self):
        self.assertTrue(
            page_primary_key_condition(self.page.pk, self.request)
        )

    def test_primary_key_invalid_string(self):
        self.assertFalse(
            page_primary_key_condition(str(self.page.pk + 1), self.request)
        )

    def test_primary_key_invalid_int(self):
        self.assertFalse(
            page_primary_key_condition(self.page.pk + 1, self.request)
        )

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            page_primary_key_condition(self.page.pk)
