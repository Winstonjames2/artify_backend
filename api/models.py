from django.db import models

class CraftItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=150)  # For product images
    promotional_content = models.CharField(max_length=200, blank=True)  # Optional promotional content
    stock_quantity = models.IntegerField(default=0)  # Track available stock
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set when the item is created
    updated_date = models.DateTimeField(auto_now=True)  # Automatically set on each update
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    category = models.ForeignKey('ItemCategory', on_delete=models.SET_NULL, null=True, related_name='items')  # Category relationship

    def __str__(self):
        return self.title


class ItemCategory(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ItemVariant(models.Model):
    craft_item = models.ForeignKey(CraftItem, on_delete=models.CASCADE, related_name='variants')  # Link to CraftItem
    name = models.CharField(max_length=100)  # E.g., "Small", "Red", etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Optional dimensions
    height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} of {self.craft_item.title}"


class ItemTag(models.Model):
    name = models.CharField(max_length=50)
    craft_items = models.ManyToManyField(CraftItem, related_name='tags')  # Link to CraftItem

    def __str__(self):
        return self.name

# shipment
class ShipmentOption(models.Model):
    SHIPMENT_CHOICES = (
        ('limited', 'Limited'),
        ('worldwide', 'WorldWide'),
    )
    craft_item = models.ForeignKey(CraftItem, on_delete=models.CASCADE, related_name='shipment_options')
    shipment_type = models.CharField(max_length=50, choices=SHIPMENT_CHOICES, default='limited')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_time_estimate = models.CharField(max_length=150)  # E.g., "2-3 weeks"
    returns_policy = models.TextField(blank=True, null=True)  # Optional returns policy

    def __str__(self):
        return f"{self.shipment_type} for {self.craft_item.title}"

