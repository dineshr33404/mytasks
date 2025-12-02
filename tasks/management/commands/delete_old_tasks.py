
from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Tasks
from datetime import timedelta

class Command(BaseCommand):
    help = "Clear completed tasks"

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=30)
        parser.add_argument("--hard", action="store_true")

    def handle(self, *args, **opts):
        cutoff = timezone.now() - timedelta(days=opts["days"])
        qs = Tasks.objects.filter(is_completed=1, updated_at__lt=cutoff)

        count = qs.count()
        if opts["hard"]:
            qs.delete()
            action = "hard-deleted"
        else:
            qs.update(is_deleted=True)
            action = "soft-deleted"

        self.stdout.write(self.style.SUCCESS(
            f"{count} tasks {action}."
        ))
