from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Tasks (models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    is_completed = models.IntegerField()
    priority = models.CharField(max_length = 10)
    due_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1) 
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TaskLogs (models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    message = models.TextField()
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

