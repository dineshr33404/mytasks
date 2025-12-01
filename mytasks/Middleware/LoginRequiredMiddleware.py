from django.shortcuts import redirect
from django.conf import settings
import re

class LoginRequiredMiddleware:
    # Define the URLs that don't require authentication
    EXEMPT_URLS = [
        r'^/login/?$',          # login page
        r'^/signup/?$',         # signup page
        r'^/register/?$',         # signup submission
        r'^/loggingin/?$',         # login submission
        r'^/admin/.*$', #default admin
        r'^/static/.*$',        # static files
        r'^/media/.*$',         # media files
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        # Compile regex patterns
        self.exempt_patterns = [re.compile(url) for url in self.EXEMPT_URLS]

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        # Check if path matches any exempt URL
        for pattern in self.exempt_patterns:
            if pattern.match('/' + path):
                return self.get_response(request)

        # If user is not authenticated, redirect to login
        if not request.user.is_authenticated:
            login_url = reverse('login') 
            return redirect(f'{login_url}?next={request.path}')

        # Continue processing request
        response = self.get_response(request)
        return response
