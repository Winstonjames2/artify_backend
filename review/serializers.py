from rest_framework import serializers
from .models import ItemReview

class ItemReviewSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')  # Use the username for display
    craft_item = serializers.ReadOnlyField(source='craft_item.title')  # Use craft item title for display

    class Meta:
        model = ItemReview
        fields = ['id', 'craft_item', 'customer', 'rating', 'description', 'created_date']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        # Assign the logged-in user as the customer
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
