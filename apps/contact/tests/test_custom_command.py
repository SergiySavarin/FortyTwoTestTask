import os

from django.test import TestCase


class CustomCommand(TestCase):
    """Test for custom command."""
    def test_custom_django_command_models_count(self):
        """Test for custom django command 'models_count'."""
        # run command models_count and take result like string from stdout
        fin, result = os.popen4('python manage.py models_count')
        self.assertIn('Owner', result.read())
