# models.py
from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
