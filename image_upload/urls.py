from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for the ImageViewSet
router = DefaultRouter()
router.register(r'api/images', views.ImageViewSet, basename='image')  # 'api/images/'

urlpatterns = [
    #  Use the router for the ImageViewSet
    path('', include(router.urls)),
    #  Admin image approval endpoint (outside the ViewSet)
    path('api/images/approve/<int:pk>/', views.approve_image, name='approve_image'),
    #  Rating endpoints (outside the ViewSet, related to a specific image)
    path('api/images/<int:pk>/rate/', views.rate_image, name='rate_image'),
    path('api/images/<int:pk>/ratings/', views.get_image_ratings, name='get_image_ratings'),
]

