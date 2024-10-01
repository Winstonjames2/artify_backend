from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import CraftItem
from account.models import CustomerProfile
from .serializers import ItemReviewSerializer

# Create a review for a craft item
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, craft_item_id):
    try:
        craft_item = CraftItem.objects.get(id=craft_item_id)
    except CraftItem.DoesNotExist:
        return Response({"error": "Craft item not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemReviewSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save(craft_item=craft_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all reviews for a specific craft item
@api_view(['GET'])
def list_reviews(request, craft_item_id):
    try:
        craft_item = CraftItem.objects.get(id=craft_item_id)
    except CraftItem.DoesNotExist:
        return Response({"error": "Craft item not found."}, status=status.HTTP_404_NOT_FOUND)
    
    reviews = craft_item.reviews.filter(is_deleted=False)
    serializer = ItemReviewSerializer(reviews, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
