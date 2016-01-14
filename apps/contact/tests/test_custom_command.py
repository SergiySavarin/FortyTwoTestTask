import subprocess

from django.test import TestCase
from fortytwo_test_task.settings import DATABASES


class CustomCommand(TestCase):
    """Test for custom command."""
    def test_custom_django_command_models_count(self):
        """Test for custom django command 'models_count'."""
        # run command models_count and take result like string from stdout
        print DATABASES
        result = subprocess.check_output(
            ['python', 'manage.py', 'models_count'],
            stderr=subprocess.STDOUT
        )
        self.assertIn('Owner', result)
