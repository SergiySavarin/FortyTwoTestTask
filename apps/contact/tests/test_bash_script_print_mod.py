import os

from django.test import TestCase


class BashScriptCustomCommand(TestCase):
    """Test for bash script for custom command."""
    def test_bash_script_run_custom_command_and_save_output_to_file(self):
        """ Test execute bash script ./print_mod
            and save output to file with name in
            format 'date_today.dat' in the same
            dir where bash script located.
        """
        # run bash script
        os.system('./print_mod.sh')
        # find saved file in and check for result
        file_names = os.popen('ls').read().split()
        output_file = [name for name in file_names if '.dat' in name]
        with open(output_file[0]) as out:
            out = out.read()
            if 'no such table: django_admin_log' in out:
                print '1'
                self.assertNotIn('Owner', out)
            else:
                print '2'
                self.assertIn('Owner', out)
        os.system('rm %s' % output_file[0])
