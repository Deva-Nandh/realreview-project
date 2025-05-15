from django.db import models
from django.utils import timezone
from datetime import timedelta

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # ImageField with an upload path
    description = models.TextField()
    location = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.image.name if self.image else 'No image'  # Display image file name or 'No image' if not uploaded

class CronJobLog(models.Model):
    # fields...
    class Meta:
        # Removed the index_together as it was causing errors
        pass
