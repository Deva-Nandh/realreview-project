from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.serializers import ValidationError
from django.db.models import Avg
from .models import Image, Rating
from .serializers import ImageSerializer, RatingSerializer
from django.shortcuts import get_object_or_404

class ImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing images.
    Provides CRUD operations and listing.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_permissions(self):
        """
        Override to set permissions based on the action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Create a new image.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Update an existing image.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "You do not have permission to update this image."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an image.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this image."},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response(
            {"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_image(request, pk):
    """
    Rate an image.
    """
    image = get_object_or_404(Image, pk=pk)
    score = request.data.get('score')

    if not score:
        return Response({'error': 'Score is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        score = int(score)  # Convert score to an integer
    except ValueError:
        return Response({'error': 'Invalid score.  Must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    if score not in range(1, 6):
        return Response({'error': 'Invalid rating score. Must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        #  Check if the user has already rated this image
        rating = Rating.objects.get(image=image, user=request.user)
        rating.score = score  # Update existing rating
        rating.save()
        return Response({'message': 'Rating updated successfully.'}, status=status.HTTP_200_OK)
    except Rating.DoesNotExist:
        #  Create a new rating
        rating = Rating.objects.create(image=image, user=request.user, score=score)
        return Response({'message': 'Rating added successfully.'}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_image_ratings(request, pk):
    """
    Get the ratings for a specific image, including the average rating.
    """
    image = get_object_or_404(Image, pk=pk)
    ratings = image.ratings.all()
    serializer = RatingSerializer(ratings, many=True)  # Use the RatingSerializer
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] or 0  # Handle no ratings

    return Response({
        'average_rating': average_rating,
        'ratings': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only admin users can access this view
def approve_image(request, pk):
    """
    Approve an image. Only accessible to admin users.
    """
    image = get_object_or_404(Image, pk=pk)
    image.approved = True
    image.save()
    return Response({'message': 'Image approved successfully.'}, status=status.HTTP_200_OK)

