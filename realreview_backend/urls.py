from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from images.views import ImageViewSet

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet, basename='image')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
