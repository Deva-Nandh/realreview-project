from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('image_upload.urls')),  # Ensures api/images/ and api/gallery/ both work
]
