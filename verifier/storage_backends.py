# your_app_name/storage_backends.py

from storages.backends.s3boto3 import S3Boto3Storage

class PublicS3Boto3Storage(S3Boto3Storage):
    default_acl = 'public-read'
