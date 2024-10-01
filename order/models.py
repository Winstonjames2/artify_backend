from django.db import models
from account.models import CustomerProfile
from api.models import CraftItem, ShipmentOption 

# Order model to link customer, items, and payment
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipment_option = models.ForeignKey(ShipmentOption, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer}"

# OrderItem model to store individual item details in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    craft_item = models.ForeignKey(CraftItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)  # Store price when purchased

    def __str__(self):
        return f"{self.quantity} of {self.craft_item.title} in Order {self.order.id}"

# Payment model to track payment details for an order
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

# Shipping model to handle shipment details
class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    tracking_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    shipping_status = models.CharField(max_length=20, default='Pending')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Shipping for Order {self.order.id}"

class Cart(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(CraftItem, through='CartItem')

    def __str__(self):
        return f"Cart of {self.customer}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    craft_item = models.ForeignKey(CraftItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.craft_item.title} in Cart"
