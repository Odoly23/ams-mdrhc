# middleware.py
from django.utils.deprecation import MiddlewareMixin
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.urls import reverse

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response


class PreviousURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the previous URL in the session
        request.session['previous_url'] = request.META.get('HTTP_REFERER', None)
        
        # Continue with the rest of the middleware chain
        response = self.get_response(request)
        
        return response



class NoBackAfterLogout(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if request.path in [reverse('login')]:
                return redirect('/')
        return None

    def process_response(self, request, response):
       
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

