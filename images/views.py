# images/views.py

from rest_framework import viewsets, filters
from .models import Image
from .serializers import ImageSerializer

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']

    def get_queryset(self):
        archived = self.request.query_params.get('archived')
        queryset = Image.objects.all()
        if archived is not None:
            queryset = queryset.filter(archived=archived.lower() == 'true')
        return queryset
