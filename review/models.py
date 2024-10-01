from django.db import models
from api.models import CraftItem
from account.models import CustomerProfile

class ItemReview(models.Model):
    craft_item = models.ForeignKey(CraftItem, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # Rating from 1 to 5
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.craft_item.title} by {self.customer.user.email}"

