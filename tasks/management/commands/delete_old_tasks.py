from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tasks.models import Tasks

class Command(BaseCommand):
    help = "Delete tasks older than 30 days"

    def handle(self, *args, **kwargs):
        # Calculate the date 30 days ago
        cutoff_date = timezone.now() - timedelta(days=30)

        # Filter tasks older than 30 days and not already deleted
        old_tasks = Tasks.objects.filter(created_at__lt=cutoff_date, is_deleted=True)
        count = old_tasks.count()
        old_tasks.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} tasks older than 30 days"))
