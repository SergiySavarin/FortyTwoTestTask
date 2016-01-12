import json

from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.test import TestCase

from models import Owner, UsersRequest
from views import requests


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
        # DB is empty
        owner0 = None
        request = HttpRequest()
        response = render(request, 'contact.html', {'owner': owner0})
        self.assertContains(response, 'Database is empty.')
        # One owner object in db
        owner1 = Owner.objects.first()
        self.assertEqual(Owner.objects.count(), 1)
        response = self.client.get(reverse('contact'))
        self.assertContains(response, owner1.first_name)
        # Two and more owner objects in db
        owner2 = Owner(
            first_name='Vasja',
            last_name='Pupkin',
            birthday='1965-12-02',
            bio='Nurilsk',
            email='rdb@yans.com',
            skype='lock_lom',
            jabber='vasja@nurilsk.com'
        )
        owner2.save()
        self.assertEqual(Owner.objects.count(), 2)
        response = self.client.get(reverse('contact'))
        self.assertContains(response, owner1.first_name)
        self.assertNotContains(response, owner2.first_name)


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
        self.assertEqual(request_1_db.request_str, request_1_pg)
        self.assertEqual(request_2_db.request_str, request_2_pg)
