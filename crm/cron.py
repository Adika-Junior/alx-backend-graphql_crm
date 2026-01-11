from datetime import datetime
import requests
from crm.models import Product

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive\n"
    
    # Optional: Verify GraphQL endpoint
    try:
        response = requests.post('http://localhost:8000/graphql', json={'query': '{ hello }'})
        if response.status_code == 200:
            message = f"{timestamp} CRM is alive and GraphQL is responsive\n"
    except:
        pass

    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(message)

def update_low_stock():
    """Update low stock products and log the updates"""
    low_stock = Product.objects.filter(stock__lt=10)
    
    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for p in low_stock:
            old_stock = p.stock
            p.stock += 10
            p.save()
            f.write(f"{timestamp} - Restocked: {p.name}, New Stock: {p.stock}\n")
