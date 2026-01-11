# Celery Setup for CRM Reports

This document provides instructions for setting up Celery with Celery Beat to generate weekly CRM reports.

## Prerequisites

- Python 3.8+
- Redis server
- Django project dependencies installed

## Installation Steps

### 1. Install Redis

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**On macOS:**
```bash
brew install redis
brew services start redis
```

**On Windows:**
Download and install Redis from: https://redis.io/download

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- celery
- django-celery-beat
- redis

### 3. Run Migrations

Celery Beat requires database tables to store periodic task schedules:

```bash
python manage.py migrate
```

### 4. Start Celery Worker

In a terminal, start the Celery worker:

```bash
celery -A crm worker -l info
```

The worker will process tasks from the queue.

### 5. Start Celery Beat

In another terminal, start Celery Beat scheduler:

```bash
celery -A crm beat -l info
```

Celery Beat will schedule the periodic tasks according to the configuration in `settings.py`.

### 6. Verify Setup

The CRM report task is scheduled to run every Monday at 6:00 AM UTC. You can verify it's working by:

1. Checking the log file:
```bash
cat /tmp/crm_report_log.txt
```

2. Monitoring the Celery worker and beat logs for task execution.

## Task Configuration

The weekly CRM report task is configured in `crm/settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

This task:
- Runs every Monday at 6:00 AM UTC
- Generates a report with total customers, orders, and revenue
- Logs the report to `/tmp/crm_report_log.txt`

## Troubleshooting

### Redis Connection Issues

If you encounter connection errors:
1. Verify Redis is running: `redis-cli ping` (should return `PONG`)
2. Check Redis URL in settings: `CELERY_BROKER_URL = 'redis://localhost:6379/0'`

### Task Not Executing

1. Ensure both Celery worker and Celery Beat are running
2. Check logs for errors
3. Verify the task is registered: `celery -A crm inspect registered`

### Database Migration Issues

If migrations fail:
```bash
python manage.py migrate django_celery_beat
```

## Production Considerations

For production environments:
- Use a process manager like Supervisor or systemd to keep Celery worker and beat running
- Configure Redis persistence
- Set up monitoring and alerting for task failures
- Use a separate Redis instance for Celery
- Configure proper logging and log rotation
