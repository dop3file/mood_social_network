from argparse import ONE_OR_MORE
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    action = models.CharField(max_length=120)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post')
    created = models.DateTimeField(auto_now_add=True)