# IP Tracking Security Project

This Django project implements IP tracking, blacklisting, geolocation, rate limiting, and anomaly detection.

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

## Features

- **IP Logging**: Every request is logged with IP, timestamp, and path
- **IP Blacklisting**: Blocked IPs get 403 Forbidden responses
- **Geolocation**: IP addresses are mapped to countries and cities
- **Rate Limiting**: Login endpoints have rate limits
- **Anomaly Detection**: Celery task flags suspicious IP behavior

## API Endpoints

- `POST /api/login/` - Login endpoint with rate limiting
- `GET/POST /api/protected/` - Protected endpoint requiring authentication

## Management Commands

Block an IP address:
```bash
python manage.py block_ip 192.168.1.100
```

## Celery Setup (Optional)

To run anomaly detection tasks:

1. Install Redis
2. Start Celery worker:
```bash
celery -A ip_security_project worker --loglevel=info
```

3. Start Celery Beat (for scheduled tasks):
```bash
celery -A ip_security_project beat --loglevel=info
```
