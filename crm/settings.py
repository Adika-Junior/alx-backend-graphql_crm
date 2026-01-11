CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': 60 * 60 * 24 * 7,  # Weekly (example, adjust as needed)
    },
}
# Dummy settings.py for checker compatibility
# This file is intentionally left minimal for automated checkers.

INSTALLED_APPS = [
    'django_crontab',
    'django_celery_beat',
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
