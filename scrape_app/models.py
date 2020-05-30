from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField('title', max_length=100)
    content = models.CharField('content', max_length=200)
    link = models.CharField('link', max_length=200)

    def __str__(self):
        return self.title
