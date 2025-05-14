from celery import shared_task
from django.utils import timezone
from .models import Image, ArchiveConfig
@shared_task
def archive_old_images_task():
    config = ArchiveConfig.objects.first()
    if not config:
        return "No config found."

    days_threshold = config.archive_after_days
    threshold_date = timezone.now() - timezone.timedelta(days=days_threshold)
    images = ImageModel.objects.filter(created_at__lt=threshold_date, archived=False)

    count = images.update(archived=True)
    return f"Archived {count} images older than {days_threshold} days."
