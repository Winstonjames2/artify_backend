from django.urls import path
from . import views

urlpatterns = [
    # Cart Endpoints
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.get_cart, name='get_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Order Endpoints
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/', views.get_orders, name='get_orders'),
    path('orders/<int:order_id>/', views.get_order, name='get_order'),
    path('orders/update/<int:order_id>/', views.update_order, name='update_order'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
]
