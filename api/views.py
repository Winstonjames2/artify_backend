from rest_framework import viewsets
from .models import CraftItem
from .serializers import CraftItemSerializer

class CraftItemViewSet(viewsets.ModelViewSet):
    queryset = CraftItem.objects.all()
    serializer_class = CraftItemSerializer
