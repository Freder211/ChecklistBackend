from django.db import models
from django.conf import settings
import uuid


class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    order = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checklist = models.ForeignKey(List, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    text = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=20, null=True, blank=True)
    time = models.CharField(max_length=20, null=True, blank=True)
    checked = models.BooleanField()
    notified = models.BooleanField()

    def __str__(self):
        return self.name + ' from ' + checklist
