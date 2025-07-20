from .models import RequestLog


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        ip_address = get_client_ip(request)
        path = request.path
        
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path
        )
        
        response = self.get_response(request)
        return response
