from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.ImageListCreateAPIView.as_view(), name='image-api'),  # View for creating images
    path('gallery/', views.image_list, name='image-list'),  # View for image listing
]
