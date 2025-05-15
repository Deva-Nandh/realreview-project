from django.core.management.base import BaseCommand
from images.models import Image
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Archive images older than 30 days'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=30)
        old_images = Image.objects.filter(uploaded_at__lte=cutoff_date, archived=False)
        count = old_images.update(archived=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully archived {count} images.'))
