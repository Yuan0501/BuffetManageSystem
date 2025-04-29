# orderApp/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from orderApp.models import Order_new, OrderItem
from app01.models import Price
from decimal import Decimal

def test_order_create_post(self):
        """POST /order/create/ should create a new order and associated order items"""
        # Simulate form data
        form_data = {
            'customer_name': 'John Doe',
            'orderitem_set-TOTAL_FORMS': '2',
            'orderitem_set-INITIAL_FORMS': '0',
            'orderitem_set-MIN_NUM_FORMS': '0',
            'orderitem_set-MAX_NUM_FORMS': '1000',
            'orderitem_set-0-item': self.p1.id,
            'orderitem_set-0-quantity': '3',
            'orderitem_set-1-item': self.p2.id,
            'orderitem_set-1-quantity': '2',
        }

        # Send POST request
        response = self.client.post(reverse('order_create'), data=form_data)

        # Check if the response redirects to the order list page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order_list'))

        # Verify that the order was created
        self.assertEqual(Order_new.objects.count(), 1)
        order = Order_new.objects.first()
        self.assertEqual(order.customer_name, 'John Doe')

        # Verify that the order items were created
        self.assertEqual(OrderItem.objects.count(), 2)
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items[0].item, self.p1)
        self.assertEqual(order_items[0].quantity, 3)
        self.assertEqual(order_items[1].item, self.p2)
        self.assertEqual(order_items[1].quantity, 2)
   
def test_order_create_invalid_post(self):
    """POST /order/create/ with invalid data should not create an order"""
    form_data = {
        'orderitem_set-TOTAL_FORMS': '1',
        'orderitem_set-INITIAL_FORMS': '0',
        'orderitem_set-MIN_NUM_FORMS': '0',
        'orderitem_set-MAX_NUM_FORMS': '1000',
        # Missing item field
    }

    response = self.client.post(self.order_create_url, data=form_data)

    self.assertEqual(response.status_code, 200)  # Form should return with errors
    self.assertFormError(response, 'form', 'orderitem_set', 'This field is required.')
    self.assertEqual(Order_new.objects.count(), 0)
    self.assertEqual(OrderItem.objects.count(), 0)


def test_order_creation():
    """Test creating an Order_new instance"""
    order = Order_new.objects.create(
        table_number=5,
        total_price=Decimal("100.50")
    )
    assert order.table_number == 5
    assert order.total_price == Decimal("100.50")
    assert order.order_time is not None  # Ensure order_time is automatically set

def test_order_default_total_price():
    """Test that the default total_price is 0"""
    order = Order_new.objects.create(
        table_number=3
    )
    assert order.total_price == 0

def test_order_string_representation():
    """Test the string representation of the Order_new model"""
    order = Order_new.objects.create(
        table_number=7,
        total_price=Decimal("50.00")
    )
    assert str(order) == f"Order {order.id} - Table {order.table_number}"


def test_order_create_post(client):
    """POST /order/create/ should create a new order and associated order items"""
    # Create Price objects for testing
    p1 = Price.objects.create(item=1, itemPrice=Decimal("10.00"))
    p2 = Price.objects.create(item=2, itemPrice=Decimal("20.00"))

    # Simulate form data
    form_data = {
        'customer_name': 'John Doe',
        'orderitem_set-TOTAL_FORMS': '2',
        'orderitem_set-INITIAL_FORMS': '0',
        'orderitem_set-MIN_NUM_FORMS': '0',
        'orderitem_set-MAX_NUM_FORMS': '1000',
        'orderitem_set-0-item': p1.id,
        'orderitem_set-0-quantity': '3',
        'orderitem_set-1-item': p2.id,
        'orderitem_set-1-quantity': '2',
    }

    # Send POST request
    response = client.post(reverse('order_create'), data=form_data)

    # Check if the response redirects to the order list page
    assert response.status_code == 302
    assert response.url == reverse('order_list')

    # Verify that the order was created
    assert Order_new.objects.count() == 1
    order = Order_new.objects.first()
    assert order.customer_name == 'John Doe'

    # Verify associated order items
    assert OrderItem.objects.count() == 2
    order_items = OrderItem.objects.filter(order=order)
    assert order_items[0].item == p1
    assert order_items[0].quantity == 3
    assert order_items[1].item == p2
    assert order_items[1].quantity == 2