from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=255, unique=True)
    subtitle=models.CharField(max_length=255, blank=True)
    slug=models.SlugField(max_length=255, unique=True)
    body=models.TextField()
    author=models.ForeignKey(User, on_delete=models.PROTECT)
    date_created=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    body=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    approved_comment=models.BooleanField(default=True)

    def __str__(self):
        return self.name
