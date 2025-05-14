# images/cron.py

from django_cron import CronJobBase, Schedule
from datetime import timedelta
from django.utils import timezone
from images.models import Image

class ArchiveOldImagesCronJob(CronJobBase):
    schedule = Schedule(run_every=timedelta(days=1))  # Run daily
    code = 'images.archive_old_images'  # Unique code for the cron job

    def do(self):
        # Get the date 30 days ago
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Archive all images older than 30 days and not already archived
        old_images = Image.objects.filter(uploaded_at__lt=thirty_days_ago, archived=False)
        old_images.update(archived=True)  # Archive them
        print(f"Archived {old_images.count()} images.")
