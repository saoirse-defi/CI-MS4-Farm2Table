from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ Storage class for static files, AWS s3 bucket. """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """ Storage class for media files, AWS s3 bucket. """
    location = settings.MEDIAFILES_LOCATION


