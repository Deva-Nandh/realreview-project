
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from images.views import ImageViewSet  # Import your ImageViewSet
from django.conf import settings
from django.conf.urls.static import static

# Create a router for your ViewSets
router = routers.DefaultRouter()
router.register(r'images', ImageViewSet, basename='image')  # Register the ImageViewSet

urlpatterns = [
    # Django admin URL
    path('admin/', admin.site.urls),

    # API URLs - use the router for ViewSets
    path('api/', include(router.urls)),

    # Serve media files during development.  This is NOT recommended for production.
    # In production, you should use a dedicated static file server (e.g., Nginx, Apache).
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Verify that the MEDIA_URL and MEDIA_ROOT settings are correctly configured in your settings.py file.
# Example:
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
