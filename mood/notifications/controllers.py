from django.contrib.auth.models import User

from .models import Notification
from posts.models import Post



def follow_notification(request, user: User) -> None:
    if Notification.objects.filter(user=user, sender=request.user).first():
        return
    notification = Notification(
        user=user,
        sender=request.user,
        action='подписался',
        post=None
    )
    notification.save()


def like_notification(request, user: User, post: Post) -> None:
    notification = Notification(
        user=user,
        sender=request.user,
        action='поставил лайк',
        post=post
    )
    notification.save()


def get_all_notifications(request):
    notifications = list(Notification.objects.filter(user=request.user).order_by('-created').all())[:20]
    return notifications