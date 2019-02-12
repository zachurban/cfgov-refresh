from importlib import import_module

from unittest import TestCase


class TestMigrationXXXX(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestMigrationXXXX, cls).setUpClass()
        cls.migration = import_module('v1.migrations.XXXX_remove_status_in_related_metadata')

    def test_remove_status_in_related_metadata(self):
        data = {
            'content': [
                {
                    'type': 'text',
                    'value': {
                        'heading': 'Category',
                        'blob': 'Some Categorization'
                    }
                },
                {
                    'type': 'text',
                    'value': {
                        'heading': 'Status',
                        'blob': 'Inactive or resolved'
                    }
                },
            ]
        }

        migrated = self.migration.remove_status_in_related_metadata(None, data)
        self.assertEqual(
            migrated,
            {
                'content': [
                    {
                        'type': 'text',
                        'value': {
                            'heading': 'Category',
                            'blob': 'Some Categorization'
                        }
                    }
                ]
            }
        )
