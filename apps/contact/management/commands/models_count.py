import sys

from django.core.management.base import BaseCommand
from django.db import models
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Print project models and count all objects per model'

    def handle(self, **options):
        for app in models.get_apps():
            for model in models.get_models(app):
                try:
                    sys.stderr.write(
                        'error: model "%s", objects: "%d"\n' % (
                            model.__name__, model.objects.count()
                        ))
                except OperationalError as err:
                    sys.stderr.write('error: %s\n' % err)
