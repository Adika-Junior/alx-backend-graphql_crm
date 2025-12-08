import django_filters
from django.db import models
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """Filter class for Customer model"""
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    email_icontains = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at']

    def filter_phone_pattern(self, queryset, name, value):
        """Custom filter to match phone numbers starting with a pattern"""
        if value:
            return queryset.filter(phone__startswith=value)
        return queryset


class ProductFilter(django_filters.FilterSet):
    """Filter class for Product model"""
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock = django_filters.NumberFilter(field_name='stock', lookup_expr='exact')
    stock__gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock__lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    low_stock = django_filters.NumberFilter(method='filter_low_stock')

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

    def filter_low_stock(self, queryset, name, value):
        """Custom filter to find products with stock below threshold"""
        threshold = value if value is not None else 10
        return queryset.filter(stock__lt=threshold)


class OrderFilter(django_filters.FilterSet):
    """Filter class for Order model"""
    total_amount__gte = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='gte'
    )
    total_amount__lte = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='lte'
    )
    order_date__gte = django_filters.DateTimeFilter(
        field_name='order_date',
        lookup_expr='gte'
    )
    order_date__lte = django_filters.DateTimeFilter(
        field_name='order_date',
        lookup_expr='lte'
    )
    customer_name = django_filters.CharFilter(
        field_name='customer__name',
        lookup_expr='icontains'
    )
    product_name = django_filters.CharFilter(
        method='filter_product_name'
    )
    product_id = django_filters.NumberFilter(
        method='filter_product_id'
    )

    class Meta:
        model = Order
        fields = ['total_amount', 'order_date']

    def filter_product_name(self, queryset, name, value):
        """Filter orders by product name"""
        if value:
            return queryset.filter(products__name__icontains=value).distinct()
        return queryset

    def filter_product_id(self, queryset, name, value):
        """Filter orders that include a specific product ID"""
        if value:
            return queryset.filter(products__id=value).distinct()
        return queryset

