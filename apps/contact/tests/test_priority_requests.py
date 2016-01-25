import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch

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
            and when priority changed to 0 show this request with
            new priority.
        """
        # Show requests with priority 1
        response = self.client.get(reverse('contact'))
        request = UsersRequest.objects.last()
        request.priority = True
        request.save()
        self.client.cookies['current_priority'] = 1
        response = self.client.get(reverse('requests'))
        self.assertContains(response, 'Priority: 1')
        self.assertNotContains(response, 'Priority: 0')
        # Make request priority false[0]
        request.priority = False
        request.save()
        self.client.cookies['current_priority'] = 0
        response = self.client.get(reverse('requests'))
        self.assertContains(response, 'Priority: 0')
        self.assertNotContains(response, 'Priority: 1')
        # Show all requests
        self.client.cookies['current_priority'] = 'all'
        response = self.client.get(reverse('requests'))
        self.assertContains(response, 'Priority: 1')
        self.assertContains(response, 'Priority: 0')

    def test_ajax_response_return_proper_count_of_requests(self):
        """ Test that ajax response return proper count of
            request objects by choosen priority.
        """
        # Make two requests and set one to 0 and second to 1 priority
        response = self.client.get(reverse('contact'))
        request = UsersRequest.objects.last()
        request.priority = False
        request.save()
        response = self.client.get(reverse('requests'))
        request = UsersRequest.objects.last()
        request.priority = True
        request.save()
        # Response return all request objects
        self.client.cookies['current_priority'] = 'all'
        count = UsersRequest.objects.count()
        response = self.client.get(
            reverse('requests'), HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        resp = json.loads(response.content)
        self.assertEqual(resp['count'], count)
        # Response return count of request objects with priority 1
        self.client.cookies['current_priority'] = '1'
        count = UsersRequest.objects.filter(priority=1).count()
        response = self.client.get(
            reverse('requests'), HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        resp = json.loads(response.content)
        self.assertEqual(resp['count'], count)
        # Response return count of request objects with priority 0
        self.client.cookies['current_priority'] = '0'
        count = UsersRequest.objects.filter(priority=0).count()
        response = self.client.get(
            reverse('requests'), HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        resp = json.loads(response.content)
        self.assertEqual(resp['count'], count)

    @patch('apps.contact.middleware.randint')
    def test_reqsts_saved_by_middlewr_have_rand_priority(self, mocked_randint):
        """Test that middle ware save requests with random priority."""
        self.assertEqual(UsersRequest.objects.count(), 0)
        for i in range(0, 3):
            mocked_randint.return_value = 0
            self.client.get(reverse('contact'))
            mocked_randint.return_value = 1
            self.client.get(reverse('requests'))
        self.client.cookies['current_priority'] = 'all'
        response = self.client.get(reverse('requests'))
        self.assertContains(response, 'Priority: 1')
        self.assertContains(response, 'Priority: 0')
