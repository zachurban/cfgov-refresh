import codecs
import errno
import json
import os
import os.path

from functools import partial

from django.core.management.base import BaseCommand
from django.core import serializers

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import get_snippet_models


outfile = partial(codecs.open, mode='wb', encoding='utf8')


def make_directory_if_needed(dirname):
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Command(BaseCommand):
    help = 'Export the wagtail tree (and supporting models)\
            into a collection of files and folders'

    def add_arguments(self, parser):
        pass

    def write_revisions(self, node, destination):
        revisions_out = outfile(destination + '/REVISIONS.json')
        revisions_json = serializers.serialize('json', node.revisions.all())
        revisions_out.write(revisions_json)
        revisions_out.close()

    def write_node(self, node, destination):
        published_out = outfile(destination + '/CURRENT.json')
        published_out.write(node.specific.to_json())
        published_out.close()

    def export_model(self, model, destination):
        with outfile(destination + '/%s_%s.json' %
                     (model._meta.app_label,
                         model._meta.model_name)) as snippet_export:
                            snippet_export.write(
                                serializers.serialize('json',
                                                      model.objects.all()))

    def export_all_snippets(self, export_dir):
        snippets_dir = export_dir + '/_SNIPPETS'
        make_directory_if_needed(snippets_dir)
        for model in get_snippet_models():
            self.export_model(model, snippets_dir)

    def export_node(self, node, destination):
        make_directory_if_needed(destination)
        self.write_node(node, destination)
        self.write_revisions(node, destination)
        for child in node.get_children():
            child_destination = os.path.join(destination + '/', child.slug)
            self.export_node(child.specific, destination=child_destination)

    def handle(self, *args, **options):
        for node in Page.get_root_nodes():
            export_dir = 'export/'
            destination = os.path.join(export_dir, node.slug)
            self.export_all_snippets(export_dir)
            self.export_node(node.specific, destination)
