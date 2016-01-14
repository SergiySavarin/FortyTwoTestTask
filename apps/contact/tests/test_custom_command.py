import subprocess

from django.db import models
from django.test import TestCase


class CustomCommand(TestCase):
    """Test for custom command."""
    def test_custom_django_command_models_count(self):
        """Test for custom django command 'models_count'."""
        # run command models_count and take result like string from stdout
        for app in models.get_apps():
            for model in models.get_models(app):
                print model.__name__
        result = subprocess.check_output(
            ['python', 'manage.py', 'models_count'],
            stderr=subprocess.STDOUT
        )
        self.assertIn('Owner', result)
