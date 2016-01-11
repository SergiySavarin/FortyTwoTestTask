import json

from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from models import Owner, UsersRequest
from views import contact, requests


class HomePageTest(TestCase):
    """Test contact home page."""
    def test_home_page_returns_correct_html(self):
        """Test site and contact.html content."""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Information')


class OwnerDataView(TestCase):
    """Test owner data view."""
    def test_storing_owner_data_to_html_page(self):
        """Test storing owner data to html."""
        owner = Owner.objects.first()
        if owner is not None:
            response = self.client.get(reverse('contact'))
            self.assertContains(response, 'Sergiy')
            self.assertContains(response, 'Savarin')
        else:
            response = self.client.get(reverse('contact'))
            self.assertContains(response, 'Database is empty.')

    def test_quantity_of_owner_objects_in_db(self):
        """Test quantity of owner objects in database."""
        owner = Owner.objects.count()
        if owner == 0:
            self.assertEqual(owner, 0)
        elif owner == 1:
            self.assertEqual(owner, 1)
        else:
            self.assertTrue(owner > 1)

class UserRequestsData(TestCase):
    """Test saving and retrieving users requests."""
    def test_saving_request_to_db_after_load_the_page_and_store_to_page(self):
        """ Test saving request data to db by middleware and storing its
            to requests.html page by the right way."""
        request = HttpRequest()
        # Make request to home page
        response1 = self.client.get(reverse('contact'))
        self.assertContains(response1, 'requests')
        response2 = self.client.get(reverse('contact'))
        self.assertContains(response2, 'requests')
        # Take last request form db
        requests_db = UsersRequest.objects.order_by('id').reverse()[:2]
        request_1_db, request_2_db = requests_db
        # Add to request META key which make is_ajax() method true
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        # Take last two requests from requests page
        requests_pg = json.loads(requests(request).content)['request']
        request_1_pg, request_2_pg = requests_pg
        # Check requests page with new requests
        self.assertEqual(request_1_db.request_str, request_1_pg[3:-4])
        self.assertEqual(request_2_db.request_str, request_2_pg[3:-4])
