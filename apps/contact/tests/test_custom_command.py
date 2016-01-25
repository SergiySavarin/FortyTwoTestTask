from django.core.management import call_command
from django.test import TestCase
from django.db import models
from StringIO import StringIO


class CustomCommand(TestCase):
    """Test for custom command."""
    def test_custom_django_command_models_count(self):
        """Test for custom django command 'models_count'."""
        # run command models_count and take result like string from stdout
        out = StringIO()
        err = StringIO()

        call_command('models_count', stdout=out, stderr=err)
        for model in models.get_models():
            self.assertIn('%s' % (model.__name__), out.getvalue())
