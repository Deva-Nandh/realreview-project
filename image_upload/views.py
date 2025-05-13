from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Image
from .serializers import ImageSerializer

# List and Create Image API View
class ImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

# Simple List Image Function
@api_view(['GET'])
def image_list(request):
    images = Image.objects.all()
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)
