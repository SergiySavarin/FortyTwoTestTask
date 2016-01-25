from django.core.management.base import BaseCommand
from django.db import models
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Print project models and count all objects per model'

    def handle(self, **options):
        std_err = ''
        for app in models.get_apps():
            for model in models.get_models(app):
                try:
                    self.stdout.write(
                        'model: "%s", objects: "%d"\n' % (
                            model.__name__, model.objects.count()
                        ))
                    std_err += (
                        'error: model: "%s", objects: "%d"\n' % (
                            model.__name__, model.objects.count()
                        ))
                except OperationalError:
                    pass
        self.stderr.write(std_err)
