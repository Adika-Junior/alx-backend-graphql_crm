from crm.models import Product
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db import transaction
from django.core.exceptions import ValidationError
import re
from decimal import Decimal

from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter


# GraphQL Types
class CustomerType(DjangoObjectType):
    """GraphQL type for Customer model"""
    class Meta:
        model = Customer
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class ProductType(DjangoObjectType):
    """GraphQL type for Product model"""
    class Meta:
        model = Product
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class OrderType(DjangoObjectType):
    """GraphQL type for Order model"""
    class Meta:
        model = Order
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


# Input Types
class CustomerInput(graphene.InputObjectType):
    """Input type for creating a customer"""
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    """Input type for creating a product"""
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int()


class OrderInput(graphene.InputObjectType):
    """Input type for creating an order"""
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


# Return Types
class CreateCustomerPayload(graphene.ObjectType):
    """Return type for CreateCustomer mutation"""
    customer = graphene.Field(CustomerType)
    message = graphene.String()


class BulkCreateCustomersPayload(graphene.ObjectType):
    """Return type for BulkCreateCustomers mutation"""
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)


class CreateProductPayload(graphene.ObjectType):
    """Return type for CreateProduct mutation"""
    product = graphene.Field(ProductType)


class CreateOrderPayload(graphene.ObjectType):
    """Return type for CreateOrder mutation"""
    order = graphene.Field(OrderType)


# Mutations
class CreateCustomer(graphene.Mutation):
    """Mutation to create a single customer"""
    class Arguments:
        input = CustomerInput(required=True)

    Output = CreateCustomerPayload

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        if not phone:
            return True
        # Match formats like +1234567890 or 123-456-7890
        pattern = r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def mutate(root, info, input):
        # Validate email uniqueness
        if Customer.objects.filter(email=input.email).exists():
            raise ValidationError("Email already exists")

        # Validate phone format
        if input.phone and not CreateCustomer.validate_phone(input.phone):
            raise ValidationError(
                "Invalid phone format. Use +1234567890 or 123-456-7890"
            )

        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone or None
        )

        return CreateCustomerPayload(
            customer=customer,
            message="Customer created successfully"
        )


class BulkCreateCustomers(graphene.Mutation):
    """Mutation to create multiple customers"""
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    Output = BulkCreateCustomersPayload

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        customers = []
        errors = []

        for idx, customer_data in enumerate(input):
            try:
                # Validate email uniqueness
                if Customer.objects.filter(email=customer_data.email).exists():
                    errors.append(
                        f"Row {idx + 1}: Email '{customer_data.email}' already exists"
                    )
                    continue

                # Validate phone format
                if customer_data.phone and not CreateCustomer.validate_phone(
                    customer_data.phone
                ):
                    errors.append(
                        f"Row {idx + 1}: Invalid phone format for '{customer_data.phone}'"
                    )
                    continue

                customer = Customer.objects.create(
                    name=customer_data.name,
                    email=customer_data.email,
                    phone=customer_data.phone or None
                )
                customers.append(customer)
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        return BulkCreateCustomersPayload(
            customers=customers,
            errors=errors
        )


class CreateProduct(graphene.Mutation):
    """Mutation to create a product"""
    class Arguments:
        input = ProductInput(required=True)

    Output = CreateProductPayload

    @staticmethod
    def mutate(root, info, input):
        # Validate price is positive
        if input.price <= 0:
            raise ValidationError("Price must be positive")

        # Validate stock is non-negative
        stock = input.stock if input.stock is not None else 0
        if stock < 0:
            raise ValidationError("Stock cannot be negative")

        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=stock
        )

        return CreateProductPayload(product=product)


class CreateOrder(graphene.Mutation):
    """Mutation to create an order with products"""
    class Arguments:
        input = OrderInput(required=True)

    Output = CreateOrderPayload

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        # Validate customer exists
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise ValidationError(f"Customer with ID '{input.customer_id}' does not exist")

        # Validate at least one product
        if not input.product_ids:
            raise ValidationError("At least one product must be selected")

        # Validate products exist
        products = []
        for product_id in input.product_ids:
            try:
                product = Product.objects.get(pk=product_id)
                products.append(product)
            except Product.DoesNotExist:
                raise ValidationError(f"Product with ID '{product_id}' does not exist")

        # Calculate total amount
        total_amount = sum(product.price for product in products)

        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount
        )
        order.products.set(products)

        return CreateOrderPayload(order=order)


class UpdateLowStockProducts(graphene.Mutation):
    """Mutation to update low stock products"""
    class Arguments:
        pass

    success = graphene.Boolean()
    updated_products = graphene.List(graphene.String)
    message = graphene.String()

    @staticmethod
    def mutate(root, info):
        low_stock = Product.objects.filter(stock__lt=10)
        names = []
        for product in low_stock:
            names.append(product.name)
            product.stock += 10
            product.save()
        
        return UpdateLowStockProducts(
            success=True,
            updated_products=names,
            message=f"Updated {len(names)} products"
        )


# Query Class
class Query(graphene.ObjectType):
    """GraphQL Query class"""
    hello = graphene.String(
        description="A simple hello query"
    )

    # Filtered queries using DjangoFilterConnectionField
    all_customers = DjangoFilterConnectionField(
        CustomerType,
        filterset_class=CustomerFilter,
        order_by=graphene.String()
    )
    all_products = DjangoFilterConnectionField(
        ProductType,
        filterset_class=ProductFilter,
        order_by=graphene.String()
    )
    all_orders = DjangoFilterConnectionField(
        OrderType,
        filterset_class=OrderFilter,
        order_by=graphene.String()
    )

    def resolve_hello(self, info):
        """Resolver for hello query"""
        return "Hello, GraphQL!"

    def resolve_all_customers(self, info, filter=None, order_by=None, **kwargs):
        """Resolver for all_customers with order_by support"""
        qs = Customer.objects.all()
        
        # Apply filters using filterset if filter is provided
        if filter:
            filterset = CustomerFilter(filter, queryset=qs)
            qs = filterset.qs
        
        # Apply ordering
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs

    def resolve_all_products(self, info, filter=None, order_by=None, **kwargs):
        """Resolver for all_products with order_by support"""
        qs = Product.objects.all()
        
        # Apply filters using filterset if filter is provided
        if filter:
            filterset = ProductFilter(filter, queryset=qs)
            qs = filterset.qs
        
        # Apply ordering
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs

    def resolve_all_orders(self, info, filter=None, order_by=None, **kwargs):
        """Resolver for all_orders with order_by support"""
        qs = Order.objects.all()
        
        # Apply filters using filterset if filter is provided
        if filter:
            filterset = OrderFilter(filter, queryset=qs)
            qs = filterset.qs
        
        # Apply ordering
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs


# Mutation Class
class Mutation(graphene.ObjectType):
    """GraphQL Mutation class"""
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

