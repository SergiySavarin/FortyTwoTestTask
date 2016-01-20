from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.contact.models import UsersRequest


class RequestsPriority(TestCase):
    """ Test request page show requsts
        accoding to priority.
    """
    def test_home_page_show_edit_link_for_request_objects_after_login(self):
        """ Test that home page show admin link for
            request objects editting after login.
        """
        # load home page like anonymous
        response = self.client.get(reverse('contact'))
        self.assertNotContains(response, '/admin/contact/usersrequest/')
        # load home page like authenticated user
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact'))
        self.assertContains(response, '/admin/contact/usersrequest/')

    def test_request_page_show_request_line_with_priority(self):
        """ Test that request page show lines with priority 1
            and doesn't show when priority changed to 0.
        """
        response = self.client.get(reverse('contact'))
        request = UsersRequest.objects.last()
        response = self.client.get(reverse('requests'))
        self.assertEqual(
            response.context['requests'][1].request_str, request.request_str
        )
        # Make request priority false
        request.priority = False
        request.save()
        response = self.client.get(reverse('requests'))
        self.assertNotEqual(
            response.context['requests'][1].request_str, request.request_str
        )
