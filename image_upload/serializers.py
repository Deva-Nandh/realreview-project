from rest_framework import serializers
from django.utils import timezone
from .models import ArchiveConfig, Image, Rating


class ArchiveConfigSerializer(serializers.ModelSerializer):
    """Serializer for Archive configuration."""
    class Meta:
        model = ArchiveConfig
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for the Rating model with user display as string."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'image', 'rating', 'timestamp']


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for Image model with basic fields."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'location', 'timestamp', 'archived']


class ImageWithRatingSerializer(serializers.ModelSerializer):
    """Serializer for Image model that includes average rating and ratings list."""
    user = serializers.StringRelatedField(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'location', 'timestamp', 'archived', 'ratings', 'average_rating']

    def get_average_rating(self, obj):
        return obj.average_rating()


class ImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading new images, attaches current user automatically."""
    class Meta:
        model = Image
        fields = ['id', 'image', 'location']

    def create(self, validated_data):
        user = self.context['request'].user
        return Image.objects.create(user=user, timestamp=timezone.now(), **validated_data)
