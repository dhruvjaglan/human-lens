from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import boto3
from django.conf import settings


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
    
    def get_private_image_url(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        object_key = str(self.image)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return url


class VerificationTaskResult(models.Model):
    tag = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    task = models.ForeignKey(TaskObject, on_delete=models.CASCADE)
    tagged_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tagged_at = models.DateTimeField(auto_now=True)


