from django.db import models

# Create your models here.

from django.db import models

class LinkSummary(models.Model):
    link = models.TextField()
    summary = models.TextField()

class TextSummary(models.Model):
    text = models.TextField()
    summary = models.TextField()