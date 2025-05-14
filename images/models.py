from django.db import models
from .validators import validate_image

class Image(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', validators=[validate_image])
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set upload time

    def __str__(self):
        return self.title
