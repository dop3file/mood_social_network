import os


ALL_EXTENSIONS = ['jpg', 'png', 'gif', 'webp']


def delete_old_avatar(instance, file_name):
    for extension in ALL_EXTENSIONS:
        try:
            os.remove(f'media/images/{instance.user.username}.{extension}')
        except FileNotFoundError:
            pass


def validate_profile_avatar(instance, file_name):
    if len(file_name.split('.')) <= 1:
        raise ValueError
    if file_name.split('.')[-1].lower() not in ALL_EXTENSIONS:
        raise ValueError
    
    
    delete_old_avatar(instance, file_name)
    return f'images/{instance.user.username}.{file_name.split(".")[-1]}'