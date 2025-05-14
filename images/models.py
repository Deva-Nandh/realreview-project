from django.db import models
from django.utils import timezone

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # Change to ImageField with an upload path
    description = models.TextField()
    location = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.image.name  # Display the image file name in the admin panel
