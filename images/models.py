
from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.location}"
