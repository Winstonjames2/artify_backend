from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CraftItemViewSet

router = DefaultRouter()
router.register(r'craft-items', CraftItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
