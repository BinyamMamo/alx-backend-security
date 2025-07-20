import requests
from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geolocation(ip_address):
    """Get geolocation data for an IP address with caching."""
    cache_key = f"geo_{ip_address}"
    geo_data = cache.get(cache_key)
    
    if geo_data is None:
        try:
            # Using ipapi.co for free geolocation (no API key required)
            response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                geo_data = {
                    'country': data.get('country_name', ''),
                    'city': data.get('city', '')
                }
            else:
                geo_data = {'country': '', 'city': ''}
        except:
            geo_data = {'country': '', 'city': ''}
        
        # Cache for 24 hours (86400 seconds)
        cache.set(cache_key, geo_data, 86400)
    
    return geo_data


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client IP
        ip_address = get_client_ip(request)
        
        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied")
        
        # Get geolocation data
        geo_data = get_geolocation(ip_address)
        
        # Log the request with geolocation
        path = request.path
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            country=geo_data.get('country', ''),
            city=geo_data.get('city', '')
        )
        
        response = self.get_response(request)
        return response
