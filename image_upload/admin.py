from django.contrib import admin
from .models import ArchiveConfig, Image, Rating


@admin.register(ArchiveConfig)
class ArchiveConfigAdmin(admin.ModelAdmin):
    list_display = ['archive_after_days']
    search_fields = ['archive_after_days']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'location', 'timestamp', 'archived']
    list_filter = ['archived', 'timestamp']
    search_fields = ['location', 'user__username']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'user', 'rating', 'timestamp']
    list_filter = ['rating']
    search_fields = ['image__id', 'user__username']
