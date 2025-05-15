from django.urls import path
from .views import (
    ArchiveConfigDetail,
    ImageListView,
    ImageUploadView,
    RatingCreateView,
    TopRatedImagesView,
)

urlpatterns = [
    path('archive-config/', ArchiveConfigDetail.as_view(), name='archive-config'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<int:pk>/rate/', RatingCreateView.as_view(), name='image-rate'),
    path('images/top-rated/', TopRatedImagesView.as_view(), name='top-rated-images'),
]
