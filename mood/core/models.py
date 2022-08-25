from django.db import models
from django.contrib.auth.models import User
from .utils import validate_profile_avatar, validate_vk_link, validate_github_link


User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to=validate_profile_avatar, null=True, blank=True)
    vk_social_link = models.CharField(max_length=150, null=True, blank=True, validators=[validate_vk_link])
    github_social_link = models.CharField(max_length=150, null=True, blank=True, validators=[validate_github_link])
    subscribers = models.ManyToManyField(User, related_name='subscribers')


class Interest(models.Model):
    title = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

