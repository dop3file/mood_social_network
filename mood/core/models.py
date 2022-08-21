from django.db import models
from django.contrib.auth.models import User
from .utils import validate_profile_avatar


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to=validate_profile_avatar, null=True, blank=True)
    