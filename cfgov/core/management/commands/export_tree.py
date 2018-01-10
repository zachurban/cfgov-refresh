import codecs
import errno
import os
import os.path

from functools import partial

from django.core.management.base import BaseCommand
from django.core import serializers
from django.apps import apps

from wagtail.wagtailcore.models import Page, PageRevision


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

    def write_revisions(self, node, destination):
        revisions_out = outfile(destination + '/REVISIONS.json')
        revisions_json = serializers.serialize('json', node.revisions.all())
        revisions_out.write(revisions_json)
        revisions_out.close()

    def write_node(self, node, destination):
        published_out = outfile(destination + '/CURRENT.json')
        published_out.write(node.specific.to_json())
        published_out.close()


    def export_node(self, node, destination):
        make_directory_if_needed(destination)
        self.write_node(node, destination)
        self.write_revisions(node, destination)
        for child in node.get_children():
            child_destination = os.path.join(destination + '/', child.slug)
            self.export_node(child.specific, destination=child_destination)

    def handle(self, *args, **options):
        export_dir = 'export/'
        models = apps.get_models(include_auto_created=True)
        exportable = [m for m in models if not issubclass(m, 
                      (Page, PageRevision))]
        export_seq = 0
        make_directory_if_needed(os.path.join(export_dir, 'models'))
        for model in exportable:
            export_location = "models/%s_%s.%s.json" % (export_seq,
                                                        model._meta.app_label,
                                                        model._meta.model_name)
            model_export = outfile(os.path.join(export_dir, export_location))
            json_serializer_class = serializers.get_serializer("json")
            serializer = json_serializer_class()
            serializer.serialize(model.objects.all(), stream=model_export)
            export_seq += 1

        for node in Page.get_root_nodes():
            destination = os.path.join(export_dir, node.slug)
            self.export_node(node.specific, destination)
