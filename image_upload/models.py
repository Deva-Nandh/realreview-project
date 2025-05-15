from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ArchiveConfig(models.Model):
    archive_after_days = models.PositiveIntegerField(
        default=30,
        help_text="Number of days after which images are automatically archived.",
    )

    def __str__(self):
        return f"Archive after {self.archive_after_days} days"


class Image(models.Model):
    image = models.ImageField(
        upload_to='images/',
        help_text="Upload the image file.",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Uploader.",
    )
    location = models.CharField(
        max_length=255,
        help_text="Location where the image was taken.",
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time when the image was uploaded.",
    )
    archived = models.BooleanField(default=False)

    def average_rating(self):
        return self.ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f"Image: {self.image.name} by {self.user.username} at {self.location} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class Rating(models.Model):
    image = models.ForeignKey(
        Image,
        related_name='ratings',
        on_delete=models.CASCADE,
        help_text="The image being rated.",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user who gave the rating.",
    )
    rating = models.PositiveIntegerField(
        help_text="The rating value (1-5).",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the rating was given.",
    )

    class Meta:
        unique_together = ('image', 'user')

    def __str__(self):
        return f"Rating {self.rating} for Image {self.image.id} by {self.user.username}"
