import codecs
import os.path
from glob import glob

from django.core.management.base import BaseCommand
from django.core import serializers
from django.db.utils import IntegrityError


from wagtail.wagtailcore.models import Page, PageRevision


class Command(BaseCommand):
    help = 'import a wagtail tree (and other models)'

    def import_node(self, path):
        json_filename = os.path.join(path, 'CURRENT.json')
        current_file = codecs.open(json_filename, encoding='utf8')
        serialized = current_file.read()
        try:
            page = Page.from_json(serialized)
            super(Page, page).save()
            page.save()
            children = glob(path + '*/')
            for child in children:
                self.import_node(child)
        except:
            print "could not unserialize %s" % json_filename

    def handle(self, *args, **options):
        import_dir = 'export/'
        wagtail_root = os.path.join(import_dir,'root/')
        self.import_node(wagtail_root) 
        model_files = glob(import_dir + 'models/*.json')
        for filename in model_files:
            with codecs.open(filename, encoding='utf8') as serialized:
                for obj in serializers.deserialize("json", serialized.read()):
                    try:
                        obj.save()
                    except IntegrityError:
                        print "integrity error while importing %s" % repr(obj)
