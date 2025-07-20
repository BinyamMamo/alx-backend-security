from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_anomalies():
    """
    Celery task to detect suspicious IP behavior.
    Runs hourly to flag IPs that:
    1. Exceed 100 requests per hour
    2. Access sensitive paths frequently
    """
    # Get the current time and 1 hour ago
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    
    # Sensitive paths to monitor
    sensitive_paths = ['/admin', '/login', '/api/login', '/admin/', '/login/']
    
    # 1. Check for IPs with more than 100 requests in the last hour
    excessive_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('id')
    ).filter(request_count__gt=100)
    
    for item in excessive_requests:
        ip_address = item['ip_address']
        request_count = item['request_count']
        
        # Create or update suspicious IP record
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_address,
            reason=f"Excessive requests: {request_count} requests in 1 hour",
            defaults={'timestamp': now}
        )
    
    # 2. Check for IPs accessing sensitive paths frequently
    sensitive_access = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').annotate(
        access_count=Count('id')
    ).filter(access_count__gt=10)  # More than 10 sensitive path accesses
    
    for item in sensitive_access:
        ip_address = item['ip_address']
        access_count = item['access_count']
        
        # Create or update suspicious IP record
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_address,
            reason=f"Frequent sensitive path access: {access_count} accesses in 1 hour",
            defaults={'timestamp': now}
        )
    
    # Return summary
    total_flagged = SuspiciousIP.objects.filter(timestamp__gte=one_hour_ago).count()
    return f"Anomaly detection completed. {total_flagged} suspicious IPs flagged in the last hour."
