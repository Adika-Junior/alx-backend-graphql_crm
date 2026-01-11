<<<<<<< HEAD
from datetime import datetime
import requests
=======

from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
>>>>>>> 95028cf (crons: scheduling and automating tasks)
from crm.models import Product

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive\n"
<<<<<<< HEAD
    
    # Optional: Verify GraphQL endpoint
    try:
        response = requests.post('http://localhost:8000/graphql', json={'query': '{ hello }'})
        if response.status_code == 200:
            message = f"{timestamp} CRM is alive and GraphQL is responsive\n"
    except:
=======

    # Optionally, verify GraphQL endpoint using gql
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql('{ hello }')
        result = client.execute(query)
        if result.get('hello'):
            message = f"{timestamp} CRM is alive and GraphQL is responsive\n"
    except Exception:
>>>>>>> 95028cf (crons: scheduling and automating tasks)
        pass

    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(message)

def update_low_stock():
<<<<<<< HEAD
    """Update low stock products and log the updates"""
    low_stock = Product.objects.filter(stock__lt=10)
    
    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for p in low_stock:
            old_stock = p.stock
            p.stock += 10
            p.save()
            f.write(f"{timestamp} - Restocked: {p.name}, New Stock: {p.stock}\n")
=======
    """Run updateLowStockProducts GraphQL mutation and log the updates"""
    from gql.transport.requests import RequestsHTTPTransport
    from gql import gql, Client
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    mutation = gql('''
        mutation {
            updateLowStockProducts {
                success
                updatedProducts
                message
            }
        }
    ''')
    try:
        result = client.execute(mutation)
        updates = result.get('updateLowStockProducts', {})
        updated_products = updates.get('updatedProducts', [])
        message = updates.get('message', '')
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            from datetime import datetime
            from gql.transport.requests import RequestsHTTPTransport
            from gql import gql, Client
            from crm.models import Product

            if updated_products:
                for name in updated_products:
                    f.write(f"{timestamp} - Restocked: {name}\n")
            f.write(f"{timestamp} - {message}\n")
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error running updateLowStockProducts: {e}\n")
>>>>>>> 95028cf (crons: scheduling and automating tasks)
