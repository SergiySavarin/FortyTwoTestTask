from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.test import TestCase

from apps.contact.models import Owner


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
