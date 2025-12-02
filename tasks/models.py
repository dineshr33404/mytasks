from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class TaskQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_completed=False, is_deleted=False)
    def visible_to(self, user, id=None):
        if user.is_superuser:
            return self.filter(owner_id=id)
        return self.active().filter(owner=user)

class Tasks (models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField()
    due_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1) 
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskQuerySet.as_manager()


class TaskLogs (models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    message = models.TextField()
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

