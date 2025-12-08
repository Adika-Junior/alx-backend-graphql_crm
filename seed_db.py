"""
Script to seed the database with sample data for testing GraphQL mutations and queries.
Run this script after migrations: python manage.py shell < seed_db.py
Or use: python manage.py runscript seed_db (if django-extensions is installed)
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order
from decimal import Decimal


def seed_database():
    """Seed the database with sample data"""
    print("Starting database seeding...")

    # Clear existing data (optional - comment out if you want to keep existing data)
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    print("Cleared existing data")

    # Create Customers
    customers_data = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol White", "email": "carol@example.com", "phone": "+1987654321"},
        {"name": "David Brown", "email": "david@example.com", "phone": "555-123-4567"},
        {"name": "Eva Davis", "email": "eva@example.com"},
    ]

    customers = []
    for data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=data["email"],
            defaults=data
        )
        customers.append(customer)
        if created:
            print(f"Created customer: {customer.name}")

    # Create Products
    products_data = [
        {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
        {"name": "Mouse", "price": Decimal("29.99"), "stock": 50},
        {"name": "Keyboard", "price": Decimal("79.99"), "stock": 30},
        {"name": "Monitor", "price": Decimal("299.99"), "stock": 15},
        {"name": "Webcam", "price": Decimal("49.99"), "stock": 25},
        {"name": "Headphones", "price": Decimal("149.99"), "stock": 20},
    ]

    products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(
            name=data["name"],
            defaults=data
        )
        products.append(product)
        if created:
            print(f"Created product: {product.name} - ${product.price}")

    # Create Orders
    orders_data = [
        {
            "customer": customers[0],  # Alice
            "products": [products[0], products[1]],  # Laptop, Mouse
        },
        {
            "customer": customers[1],  # Bob
            "products": [products[2], products[3]],  # Keyboard, Monitor
        },
        {
            "customer": customers[0],  # Alice
            "products": [products[4]],  # Webcam
        },
        {
            "customer": customers[2],  # Carol
            "products": [products[0], products[5]],  # Laptop, Headphones
        },
    ]

    for data in orders_data:
        customer = data["customer"]
        order_products = data["products"]
        total_amount = sum(p.price for p in order_products)

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount
        )
        order.products.set(order_products)
        print(f"Created order #{order.id} for {customer.name} - Total: ${total_amount}")

    print("\nDatabase seeding completed!")
    print(f"Created {Customer.objects.count()} customers")
    print(f"Created {Product.objects.count()} products")
    print(f"Created {Order.objects.count()} orders")


if __name__ == "__main__":
    seed_database()

