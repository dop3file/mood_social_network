from django.conf import settings


def validate_post_image(instance, file_name):
    if len(file_name.split('.')) <= 1:
        raise ValueError
    if file_name.split('.')[-1].lower() not in settings.ALL_EXTENSIONS:
        raise ValueError

    return f'posts/{instance.id}.{file_name.split(".")[-1]}'

    