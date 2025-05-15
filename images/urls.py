# realreview_backend/images/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageMetadataViewSet

router = DefaultRouter()
router.register(r'images', ImageMetadataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
