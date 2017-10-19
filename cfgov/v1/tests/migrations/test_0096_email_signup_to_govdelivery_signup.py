# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib
from unittest import TestCase

import mock
from wagtail.wagtailcore.models import Page, PageRevision


class EmailSignupToGovDeliverySignupTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(EmailSignupToGovDeliverySignupTestCase, cls).setUpClass()
        cls.migration = importlib.import_module(
            'v1.migrations.0095_email_signup_to_govdelivery_signup'
        )

    def test_forwards(self):
        """ Forward migration """
        data = {
            'heading': u'Stay Informed',
            'text': u'Subscribe to our newsletter.',

            'gd_code': u'GDCODE',
            'form_field': [{
                'type': u'email',
                'label': u'Email address',
                'info': u'<a href="/privacy/privacy-policy/">Privacy</a></p>',
                'btn_text': u'Sign up',
                'is_required': None,
                'placeholder': u'mail@example.com'
            }],
            'form_fields': [{}],

            'privacy_act_statement': None
        }
        migrated = self.migration.migrate_email_signup_forwards(None, data)
        self.assertEqual(
            migrated['form_fields'],
            [{
                'type': 'email',
                'label': 'Email address',
                'gd_code': 'GDCODE',
            }]
        )

    def test_backwards(self):
        """ Backwards migration """
        data = {
            'heading': u'Stay Informed',
            'text': u'Subscribe to our newsletter.',
            'gd_code': None,
            'form_field': [{}],
            'form_fields': [{
                'type': 'email',
                'label': 'Email address',
                'gd_code': 'GDCODE',
            }],
            'privacy_act_statement': None
        }
        migrated = self.migration.migrate_email_signup_backwards(None, data)
        self.assertEqual(
            migrated['form_field'],
            [{
                'type': u'email',
                'label': u'Email address',
                'info': None,
                'btn_text': u'Sign up',
                'is_required': None,
                'placeholder': u'mail@example.com'
            }]
        )
        self.assertEqual(migrated['gd_code'], 'GDCODE')
