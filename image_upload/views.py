from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ArchiveConfig, Image, Rating
from .serializers import (
    ArchiveConfigSerializer,
    ImageSerializer,
    ImageWithRatingSerializer,
    ImageUploadSerializer,
    RatingSerializer,
)


class ArchiveConfigDetail(generics.RetrieveUpdateAPIView):
    queryset = ArchiveConfig.objects.all()
    serializer_class = ArchiveConfigSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return ArchiveConfig.objects.first()


class ImageListView(generics.ListAPIView):
    queryset = Image.objects.all().order_by('-timestamp')
    serializer_class = ImageWithRatingSerializer
    permission_classes = [permissions.AllowAny]


class ImageUploadView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TopRatedImagesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        images = Image.objects.all()
        images = sorted(images, key=lambda img: img.average_rating(), reverse=True)[:10]
        serializer = ImageWithRatingSerializer(images, many=True)
        return Response(serializer.data)
