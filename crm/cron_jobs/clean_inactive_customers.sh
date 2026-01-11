#!/bin/bash

# Navigate to the project directory
cd /home/j_view/Projects/alx-backend-graphql_crm

one_year_ago = timezone.now() - timedelta(days=365)
# Use Django's shell to execute Python logic
python3 manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)
# Find customers with no orders since one year ago
inactive_customers = Customer.objects.exclude(order__order_date__gte=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()

# Log the results
with open('/tmp/customer_cleanup_log.txt', 'a') as f:
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"{timestamp} - Deleted {count} inactive customers\n")
print(f"Deleted {count} inactive customers")
EOF
