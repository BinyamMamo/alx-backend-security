from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
import json


@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    """
    Login view with rate limiting.
    Authenticated users: 10 requests/minute
    Anonymous users: 5 requests/minute
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'}, status=405)


@csrf_exempt
@ratelimit(key='ip', rate='10/m', method=['GET', 'POST'])
def authenticated_view(request):
    """
    A view that requires authentication with rate limiting.
    Rate limit: 10 requests/minute for authenticated users
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'success': True, 
            'message': f'Hello {request.user.username}!',
            'user_id': request.user.id
        })
    else:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
