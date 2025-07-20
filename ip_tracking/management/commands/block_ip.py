from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP
import re


class Command(BaseCommand):
    help = 'Block an IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to block')

    def handle(self, *args, **options):
        ip_address = options['ip_address']

        # Simple IP address validation regex
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

        if not re.match(ip_pattern, ip_address):
          self.stdout.write(self.style.ERROR(f'Invalid IP address format: {ip_address}'))
          return
        
        blocked_ip, created = BlockedIP.objects.get_or_create(ip_address=ip_address)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
        else:
            self.stdout.write(self.style.WARNING(f'IP {ip_address} is already blocked'))
