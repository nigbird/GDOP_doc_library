# filepath: /c:/Users/hp/myproject/doc_library/models.py
from django.db import models
from django.contrib.auth.models import User

class UploadFolder(models.Model):
    name = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(UploadFolder, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    version_count = models.IntegerField(default=1)

    def __str__(self):
        return self.title