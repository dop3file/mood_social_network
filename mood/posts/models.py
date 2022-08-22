from django.db import models
from django.contrib.auth.models import User
from .utils import validate_post_image


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)
    image = models.ImageField(upload_to=validate_post_image, null=True, blank=True)
    type_mood = models.BooleanField()
