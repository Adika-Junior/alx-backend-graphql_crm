<<<<<<< HEAD
=======
import requests
>>>>>>> 95028cf (crons: scheduling and automating tasks)
import requests
from celery import shared_task
from datetime import datetime
from django.db.models import Sum
from crm.models import Customer, Order

@shared_task
def generate_crm_report():
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
    
    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(report)
