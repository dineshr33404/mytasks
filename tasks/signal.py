from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Tasks, TaskLogs
from mytasks.Middleware.CurrentUserMiddleware import get_current_user

@receiver(post_save, sender=Tasks)
def task_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New task created: {instance.title}")
        TaskLogs.objects.create(
            task=instance,
            actor=get_current_user(),
            message=f"Task created on {instance.owner.username}"
        )
    else:
        print(f"Task updated: {instance.title}")
        TaskLogs.objects.create(
            task=instance,
            actor=get_current_user(),
            message=f"Task updated on {instance.owner.username}"
        )


@receiver(pre_delete, sender=Tasks)
def task_deleted(sender, instance, **kwargs):
    print(f"Task deleted: {instance.title}")
