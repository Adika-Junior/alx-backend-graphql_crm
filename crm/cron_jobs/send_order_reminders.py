import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# Setup the GraphQL client
transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')

# Query for orders within the last 7 days
query = gql("""
    query($orderDateGte: DateTime) {
        allOrders(filter: { orderDateGte: $orderDateGte }) {
            edges {
                node {
                    id
                    orderDate
                    customer {
                        email
                    }
                }
            }
        }
    }
""")

def run():
    try:
        result = client.execute(query, variable_values={"orderDateGte": seven_days_ago})
        
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            orders = result.get('allOrders', {}).get('edges', [])
            for edge in orders:
                order = edge['node']
                f.write(f"{timestamp} - ID: {order['id']}, Email: {order['customer']['email']}\n")
        
        print("Order reminders processed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
