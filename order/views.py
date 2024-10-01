from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Order, OrderItem, Payment, Shipping, Cart, CartItem
from api.models import CraftItem
from .serializers import OrderSerializer, CartSerializer, CartItemSerializer

# Create an Order from the Cart
@api_view(['POST'])
def create_order(request):
    try:
        # Fetch the customer's cart
        cart = Cart.objects.get(customer=request.user.customerprofile)

        # Create an order
        order = Order.objects.create(
            customer=request.user.customerprofile,
            total_price=cart_total(cart),  # Calculate total price from the cart
            shipment_option=request.data.get('shipment_option')
        )

        # Move cart items to the Order
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                craft_item=cart_item.craft_item,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.craft_item.price
            )

        # Clear the cart after creating the order
        cart.cart_items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found."}, status=status.HTTP_400_BAD_REQUEST)

# Helper function to calculate cart total price
def cart_total(cart):
    total = 0
    for cart_item in cart.cart_items.all():
        total += cart_item.craft_item.price * cart_item.quantity
    return total

# Retrieve all Orders or filter by customer
@api_view(['GET'])
def get_orders(request):
    if request.query_params.get('customer_id'):
        orders = Order.objects.filter(customer_id=request.query_params.get('customer_id'))
    else:
        orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve a specific order
@api_view(['GET'])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

# Update an Order
@api_view(['PUT'])
def update_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

# Delete an Order
@api_view(['DELETE'])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

# Add an item to the Cart
@api_view(['POST'])
def add_to_cart(request):
    customer = request.user.customerprofile
    craft_item_id = request.data.get('craft_item_id')
    quantity = request.data.get('quantity', 1)

    try:
        # Get or create the cart for the customer
        cart, _ = Cart.objects.get_or_create(customer=customer)

        # Get the craft item
        craft_item = CraftItem.objects.get(id=craft_item_id)

        # Create or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, craft_item=craft_item)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({"message": "Item added to cart successfully."}, status=status.HTTP_200_OK)
    except CraftItem.DoesNotExist:
        return Response({"error": "Craft item not found."}, status=status.HTTP_404_NOT_FOUND)

# Retrieve the Cart
@api_view(['GET'])
def get_cart(request):
    try:
        cart = Cart.objects.get(customer=request.user.customerprofile)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

# Remove an item from the Cart
@api_view(['DELETE'])
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
