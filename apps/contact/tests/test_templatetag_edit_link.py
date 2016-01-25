from django.core.urlresolvers import reverse
from django.test import TestCase


class AdminEditLink(TestCase):
    """ Test own template tag "object_link"
        render admin link for editting object.
    """
    def test_home_page_show_edit_link_after_login(self):
        """ Test that home page show admin link for
            object editting after login.
        """
        # load home page like anonymous
        response = self.client.get(reverse('contact'))
        self.assertNotContains(response, '/admin/contact/owner/1/')
        # load home page like authenticated user
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact'))
        self.assertContains(response, '/admin/contact/owner/1/')
