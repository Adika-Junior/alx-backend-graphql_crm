# ALX Backend GraphQL CRM

A Django-based CRM system with GraphQL API implementation using graphene-django.

## Features

- GraphQL API with queries and mutations
- Customer, Product, and Order management
- Advanced filtering with django-filter
- Bulk operations support
- Comprehensive validation and error handling

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd alx-backend-graphql_crm
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. (Optional) Seed the database:
```bash
python manage.py shell < seed_db.py
```

6. Start the development server:
```bash
python manage.py runserver
```

## GraphQL Endpoint

Access the GraphQL API at: `http://localhost:8000/graphql`

GraphiQL interface is available at the same URL for interactive query testing.

## GraphQL Queries

### Hello Query (Task 0)
```graphql
query {
  hello
}
```

### Filter Customers
```graphql
query {
  allCustomers(filter: { nameIcontains: "Ali", createdAtGte: "2025-01-01" }) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

### Filter Products
```graphql
query {
  allProducts(filter: { priceGte: 100, priceLte: 1000 }, orderBy: "-stock") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Filter Orders
```graphql
query {
  allOrders(filter: { customerName: "Alice", productName: "Laptop", totalAmountGte: 500 }) {
    edges {
      node {
        id
        customer {
          name
        }
        products {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

## GraphQL Mutations

### Create Customer
```graphql
mutation {
  createCustomer(input: {
    name: "Alice"
    email: "alice@example.com"
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
      phone
    }
    message
  }
}
```

### Bulk Create Customers
```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob", email: "bob@example.com", phone: "123-456-7890" },
    { name: "Carol", email: "carol@example.com" }
  ]) {
    customers {
      id
      name
      email
    }
    errors
  }
}
```

### Create Product
```graphql
mutation {
  createProduct(input: {
    name: "Laptop"
    price: 999.99
    stock: 10
  }) {
    product {
      id
      name
      price
      stock
    }
  }
}
```

### Create Order
```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    productIds: ["1", "2"]
  }) {
    order {
      id
      customer {
        name
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
  }
}
```

## Project Structure

```
alx-backend-graphql_crm/
├── alx_backend_graphql_crm/    # Main project directory
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL configuration
│   └── schema.py               # Main GraphQL schema
├── crm/                         # CRM app
│   ├── models.py               # Django models
│   ├── schema.py               # GraphQL types, queries, mutations
│   ├── filters.py              # Django-filter filter classes
│   └── admin.py                # Django admin configuration
├── seed_db.py                  # Database seeding script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Models

### Customer
- `name`: CharField (required)
- `email`: EmailField (required, unique)
- `phone`: CharField (optional)
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

### Product
- `name`: CharField (required)
- `price`: DecimalField (required, positive)
- `stock`: IntegerField (optional, default: 0, non-negative)
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

### Order
- `customer`: ForeignKey to Customer (required)
- `products`: ManyToManyField to Product (required)
- `total_amount`: DecimalField (calculated)
- `order_date`: DateTimeField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

## Filtering Features

### Customer Filters
- `name`: Case-insensitive partial match
- `email`: Case-insensitive partial match
- `created_at__gte`: Filter by creation date (greater than or equal)
- `created_at__lte`: Filter by creation date (less than or equal)
- `phone_pattern`: Custom filter for phone number pattern matching

### Product Filters
- `name`: Case-insensitive partial match
- `price__gte`: Filter by minimum price
- `price__lte`: Filter by maximum price
- `stock__gte`: Filter by minimum stock
- `stock__lte`: Filter by maximum stock
- `low_stock`: Custom filter for products with stock below threshold

### Order Filters
- `total_amount__gte`: Filter by minimum total amount
- `total_amount__lte`: Filter by maximum total amount
- `order_date__gte`: Filter by order date (greater than or equal)
- `order_date__lte`: Filter by order date (less than or equal)
- `customer_name`: Filter by customer name (case-insensitive)
- `product_name`: Filter by product name (case-insensitive)
- `product_id`: Filter orders containing a specific product

## Validation

### Customer Validation
- Email must be unique
- Phone format validation: `+1234567890` or `123-456-7890`

### Product Validation
- Price must be positive
- Stock must be non-negative

### Order Validation
- Customer must exist
- Products must exist
- At least one product must be selected
- Total amount is automatically calculated

## Error Handling

All mutations include comprehensive error handling:
- Duplicate email errors
- Invalid phone format errors
- Missing required fields
- Invalid IDs (customer/product not found)
- Validation errors with user-friendly messages

## Testing

Use GraphiQL at `http://localhost:8000/graphql` to test all queries and mutations interactively.

## License

This project is part of the ALX Backend specialization curriculum.

