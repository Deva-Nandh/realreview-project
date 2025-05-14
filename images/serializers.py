from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(read_only=True)  # Ensure read-only

    class Meta:
        model = Image
        fields = ['id', 'title', 'description', 'image', 'uploaded_at']
