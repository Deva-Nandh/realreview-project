from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.CharField(max_length=100)  # Text field (no ForeignKey)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
