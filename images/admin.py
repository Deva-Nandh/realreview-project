from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'uploaded_at', 'approved','archived')
    list_filter = ('approved','archived')  # Filter images by approval status
    actions = ['approve_images', 'disapprove_images','archive_images']  # Add custom actions
    
    def approve_images(self, request, queryset):
        queryset.update(approved=True)  # Approve selected images
    approve_images.short_description = "Approve selected images"

    def disapprove_images(self, request, queryset):
        queryset.update(approved=False)  # Disapprove selected images
    disapprove_images.short_description = "Disapprove selected images"
    
    def archive_images(self, request, queryset):
        queryset.update(archived=True)
    archive_images.short_description = "Archive selected images"

admin.site.register(Image, ImageAdmin)
