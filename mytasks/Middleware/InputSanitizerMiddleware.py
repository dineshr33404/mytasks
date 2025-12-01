from django.http import HttpResponseBadRequest
import re

class InputSanitizerMiddleware:

    # Simple patterns to block
    MALICIOUS_PATTERNS = [
        r'<script.*?>.*?</script>',  # XSS scripts
        r'javascript:',              # JS injection
        r'on\w+=".*?"',              # inline event handlers
        r'drop\s+table',             # SQL injection
        r'select\s+.*\s+from',       # SQL injection
        r'--',                       # SQL comment
        r';',                        # SQL statement separator
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        # Compile patterns for faster matching
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.MALICIOUS_PATTERNS]

    def __call__(self, request):
        # Combine all GET and POST parameters
        all_params = {}
        all_params.update(request.GET.dict())
        all_params.update(request.POST.dict())

        # Check each value for malicious patterns
        for key, value in all_params.items():
            for pattern in self.patterns:
                if pattern.search(str(value)):
                    return HttpResponseBadRequest(f"Malicious input detected in '{key}'")

        # If safe, continue the request
        response = self.get_response(request)
        return response
