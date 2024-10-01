from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('account.urls')),
    path('', include('order.urls')),
    path('', include('review.urls'))
]
