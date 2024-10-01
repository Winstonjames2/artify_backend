from django.urls import path
from .views import create_review, list_reviews

urlpatterns = [
    path('craft_item/<int:craft_item_id>/reviews/', list_reviews, name='list_reviews'),
    path('craft_item/<int:craft_item_id>/reviews/create/', create_review, name='create_review'),
]
