from django.db import models

# Create your models here.
class Status(models.Model):

    status = models.CharField(max_length=256)
    key = models.CharField(max_length=256)
    create_time = models.CharField(max_length=14)
    binding = models.TextField(max_length=65535, null=True, blank=True)