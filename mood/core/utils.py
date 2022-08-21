import os


def validate_profile_avatar(instance, file_name):
    if len(file_name.split('.')) <= 1:
        raise ValueError
    if file_name.split('.')[-1].lower() not in ['jpg', 'png', 'gif']:
        raise ValueError
    
    return f'images/{instance.user.username}.{file_name.split(".")[1]}'