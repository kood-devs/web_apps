from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField('title', max_length=100)
    content = models.CharField('content', max_length=500)

    def __str__(self):
        return self.title
