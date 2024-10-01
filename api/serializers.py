from rest_framework import serializers
from .models import CraftItem

class CraftItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CraftItem
        fields = '__all__'
