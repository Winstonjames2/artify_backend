from django.contrib import admin
from .models import CraftItem, ItemCategory, ItemVariant, ShipmentOption

admin.site.register(CraftItem)
admin.site.register(ItemCategory)
admin.site.register(ItemVariant)
admin.site.register(ShipmentOption)
