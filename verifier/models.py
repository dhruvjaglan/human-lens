from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    is_available = models.BooleanField(default=False)
    is_annotator = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    ongoing_task = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Company(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    logo = models.FileField(upload_to='company', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, unique=True)


class TaskObject(models.Model):
    PENDING = 'P'
    COMPLETED = 'C'

    TASK_STATE = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    details = models.TextField()
    image = models.ImageField(upload_to='tasks', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    options = models.JSONField(default=list)
    state = models.CharField(
        max_length=1, choices=TASK_STATE, default=PENDING)

class VerificationTaskResult(models.Model):
    tag = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    task = models.ForeignKey(TaskObject, on_delete=models.CASCADE)
    tagged_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tagged_at = models.DateTimeField(auto_now_add=True)


