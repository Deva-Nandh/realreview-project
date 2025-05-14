k# image_upload/serializers.py
from rest_framework import serializers
from .models import Image  # Assuming you have an Image model for your uploaded images

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'description', 'image', 'uploaded_at')
