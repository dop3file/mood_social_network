from django.conf import settings
from django.db.models import Q
import os


def delete_old_avatar(instance, file_name):
    for extension in settings.ALL_EXTENSIONS:
        try:
            os.remove(f'media/images/{instance.user.username}.{extension}')
        except FileNotFoundError:
            pass


def validate_profile_avatar(instance, file_name):
    if len(file_name.split('.')) <= 1:
        raise ValueError
    if file_name.split('.')[-1].lower() not in settings.ALL_EXTENSIONS:
        raise ValueError
    
    delete_old_avatar(instance, file_name)
    return f'images/{instance.user.username}.{file_name.split(".")[-1]}'


def validate_vk_link(link: str):
    if link.startswith('vk.com/') or link.startswith('https://vk.com/'):
        return True
    raise ValueError


def validate_github_link(link: str):
    if link.startswith('github.com/') or link.startswith('https://github.com/'):
        return True
    raise ValueError


def search_post(post_instance, search_text):
    return post_instance.objects.filter(
            Q(text__icontains=search_text) | Q(user__username__icontains=search_text)
        ).order_by('-date_post')
    
