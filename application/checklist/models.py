from django.db import models

class List(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=20) 
    order = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    checklist = models.ForeignKey(List, on_delete=models.CASCADE)
    name = models.CharField(max_length=20) 
    text = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=20, null=True, blank=True) 
    time = models.CharField(max_length=20, null=True, blank=True) 
    checked = models.BooleanField()
    notified = models.BooleanField()

    def __str__(self):
        return self.name + ' from ' + checklist