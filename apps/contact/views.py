import json
import signals  # noqa

from forms import EditContactForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils import size, resize

from fortytwo_test_task.settings import MEDIA_ROOT
from .models import Owner, UsersRequest


def contact(request):
    """View for contact.html root page."""
    # Take owner data from the database
    owner = Owner.objects.first()
    requests = UsersRequest()
    data = {'owner': owner, 'requests': requests}
    return render(request, 'contact.html', data)


def requests(request):
    """View for last ten requests to server."""
    # Get request priority from cookies
    prior = request.COOKIES.get('current_priority')
    if prior != 'all':
        # Take last ten requests from the database and sort its by id
        requests = UsersRequest.objects.filter(priority=prior)
        requests = requests.order_by('-id')[:10]
        # Quantity of requests
        count = UsersRequest.objects.filter(priority=prior).count()
    else:
        # Take last ten requests from the database and sort its by id
        requests = UsersRequest.objects.order_by('-id')[:10]
        # Quantity of requests
        count = UsersRequest.objects.count()
    # if request is ajax, prepare requests and
    # send its in json format
    if request.is_ajax():
        response_data = {
            'request': [
                ('Priority: %s, %s') % (int(req.priority), req.request_str)
                for req in requests
            ],
            'count': count
        }
        return HttpResponse(json.dumps(response_data))
    return render(request, 'requests.html', {'requests': requests})


@login_required
def edit_contact(request):
    """View for editing owner data."""
    owner = Owner.objects.first()
    if request.method == 'GET':
        form = EditContactForm(instance=owner)
        return render(request, 'edit_contact.html', {'form': form})
    elif request.method == 'POST':
        if request.POST.get('save_button') is not None:
            form = EditContactForm(request.POST, request.FILES, instance=owner)
            if form.is_valid():
                owner = form.save()
                owner.save()
                # Take owner photo path
                photo_path = '%s/%s' % (MEDIA_ROOT, owner.photo)
                # Check photo size, if not 200x200px, resize it
                if not size(photo_path):
                    resize(photo_path)
            else:
                if request.is_ajax():
                    errors = {}
                    for error in form.errors:
                        errors[error] = form.errors[error]
                    return HttpResponseBadRequest(json.dumps(errors))
            return HttpResponseRedirect(reverse('edit_contact'))
        else:
            form = EditContactForm(request.POST)
            return render(request, 'edit_contact.html', {'form': form})


@login_required
def bar_shell(request):
    """Barista shell using."""
    if request.method == 'POST':
        command = request.POST.get('command')
        import subprocess
        try:
            answer = subprocess.check_output(
                command, stderr=subprocess.STDOUT, shell=True
            )
        except subprocess.CalledProcessError as err:
            answer = err.output
        answer = answer.split('\n')
        if request.is_ajax():
            response_data = {
                'answer': [ans for ans in answer] 
            }
            return HttpResponse(json.dumps(response_data))
        return render(request, 'terminal.html', {'answer': answer})
    return render(request, 'terminal.html')
