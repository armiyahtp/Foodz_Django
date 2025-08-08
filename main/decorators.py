import json

from django.http import HttpResponse
from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect


def allow_super(function):
    def wrap(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_superuser:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'status': 'error',
                    'title': 'Unauthorized Access',
                    'message': 'You cannot perform this action.',
                }
                return HttpResponse(json.dumps(response_data),content_type='application/json',)
            
            else:
                return HttpResponseRedirect(reverse('manager:logout'))
    
        return function(request, *args, **kwargs)

    return wrap


def allow_store(function):
    def wrap(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_store:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'status': 'error',
                    'title': 'Unauthorized Access',
                    'message': 'You cannot perform this action.',
                }
                return HttpResponse(json.dumps(response_data),content_type='application/json',)
            
            else:
                return HttpResponseRedirect(reverse('restaurant:logout'))

        return function(request, *args, **kwargs)

    return wrap



def allow_agent(function):
    def wrap(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_agent:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'status': 'error',
                    'title': 'Unauthorized Access',
                    'message': 'You cannot perform this action.',
                }
                return HttpResponse(json.dumps(response_data),content_type='application/json',)
            
            else:
                return HttpResponseRedirect(reverse('agent:logout'))

        return function(request, *args, **kwargs)

    return wrap