from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Image(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)  # Admin approval field
    archived = models.BooleanField(default=False)  # Track archived status
    location = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else f"Image uploaded by {self.user.username} at {self.uploaded_at}"

    class Meta:
        ordering = ['-uploaded_at']


class Rating(models.Model):
    image = models.ForeignKey(Image, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'image')  # Ensure a user can only rate an image once

    def __str__(self):
        return f"{self.user.username} - {self.score} for {self.image.title}"
