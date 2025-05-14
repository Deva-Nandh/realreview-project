from django.db import models

class ArchiveConfig(models.Model):
    archive_after_days = models.PositiveIntegerField(default=30, help_text="Number of days after which images are archived.")

    def __str__(self):
        return f"Archive after {self.archive_after_days} days"


class Image(models.Model):
    image = models.ImageField(upload_to='images/', help_text="Upload the image file.")
    user = models.CharField(max_length=100, help_text="Uploader's name.")
    location = models.CharField(max_length=255, help_text="Location where the image was taken.")
    timestamp = models.DateTimeField(help_text="Date and time when the image was created or uploaded.")

    def __str__(self):
        return f"Image by {self.user} at {self.location} on {self.timestamp.strftime('%Y-%m-%d')}"
