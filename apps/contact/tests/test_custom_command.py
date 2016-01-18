from django.core.management import call_command
from django.test import TestCase
from StringIO import StringIO


class CustomCommand(TestCase):
    """Test for custom command."""
    def test_custom_django_command_models_count(self):
        """Test for custom django command 'models_count'."""
        # run command models_count and take result like string from stdout
        out = StringIO()
        call_command('models_count', stderr=out)
        self.assertIn('Owner', out.getvalue())
