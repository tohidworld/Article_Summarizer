from django.db import models

class LinkSummary(models.Model):
    link = models.TextField()
    summary = models.TextField()